"""Browser regression tests for Team 04 white-box BookStack workflows."""

import os
import re
import subprocess
import tempfile
import time
import unittest
from contextlib import contextmanager
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


APP = Path(__file__).resolve().parents[2]


@contextmanager
def fresh_app():
    with tempfile.TemporaryDirectory() as temp:
        log = Path(temp) / "server.log"
        with log.open("w") as output:
            server = subprocess.Popen(
                ["node", "backend/dist/server.js"],
                cwd=APP,
                env={**os.environ, "HOST": "127.0.0.1", "PORT": "0", "DATABASE_URL": ":memory:"},
                stdout=output,
                stderr=subprocess.STDOUT,
            )
        try:
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline and server.poll() is None:
                match = re.search(r"Application listening at http://localhost:(\d+)", log.read_text())
                if match:
                    yield f"http://127.0.0.1:{match[1]}"
                    return
                time.sleep(0.05)
            raise RuntimeError(f"BookStack failed to start. Run npm run build first.\n{log.read_text()}")
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()


def control(scope, role, name):
    return scope.get_by_role(role, name=name, exact=True)


def entry(scope, name):
    return control(scope, "link", name).or_(control(scope, "button", name))


def create_book(page, name):
    control(page, "link", "Books").click()
    entry(page, "Create New Book").click()
    control(page, "textbox", "Name").fill(name)
    control(page, "button", "Save Book").click()
    expect(control(page, "heading", name)).to_be_visible()


def login(page):
    page.goto("/")
    control(page, "link", "Login").click()
    control(page, "textbox", "Email").fill("bookstack_user@example.com")
    page.get_by_label("Password", exact=True).fill("Password123!")
    control(page, "button", "Login").click()
    expect(control(page, "region", "My Recent Drafts")).to_be_visible()


class Team04Workflows(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        playwright = sync_playwright().start()
        cls.addClassCleanup(playwright.stop)
        cls.browser = playwright.chromium.launch(
            executable_path=os.environ.get("CHROMIUM_EXECUTABLE") or None,
        )
        cls.addClassCleanup(cls.browser.close)

    def setUp(self):
        self.base_url = self.enterContext(fresh_app())
        context = self.browser.new_context(base_url=self.base_url, viewport={"width": 1440, "height": 900})
        self.addCleanup(context.close)
        self.page = context.new_page()

    def test_most_viewed_favorite(self):
        page = self.page
        login(page)
        names = ["Atlas", "Birch", "Cedar", "Dune", "Elm"]
        for name in names:
            create_book(page, name)
            control(page, "button", "Favorite").click()
            expect(control(page, "button", "Unfavorite")).to_have_attribute("aria-pressed", "true")

        for _ in range(6):
            control(page, "link", "Books").click()
            entry(control(page, "region", "Book list"), "Atlas").click()
            expect(control(page, "heading", "Atlas")).to_be_visible()

        page.goto("/")
        panel = control(page, "region", "My Most Viewed Favorites")
        expect(panel).to_be_visible()
        shown = [name for name in names if entry(panel, name).is_visible()]
        self.assertLessEqual(len(shown), 4)
        # All five remain favorites. Only Atlas has additional visits.
        entry(page, "My Favourites").click()  # Label in the course target.
        for name in names:
            expect(entry(page, name)).to_be_visible()
        self.assertIn("Atlas", shown, f"Homepage showed {shown}. All five exist in My Favourites.")

    def test_history_returns_to_selected_draft(self):
        page = self.page
        login(page)
        title = control(page, "textbox", "Page title")
        body = control(page, "textbox", "Write your page content here...")
        book = "Field notes"
        create_book(page, book)
        for name in ["North", "South"]:
            control(page, "button", "New Page").click()
            title.fill(name)
            body.fill(f"{name} observations")
            control(page, "button", "Save Draft").click()
            expect(entry(control(page, "region", "Page list"), name)).to_be_visible()

        entry(control(page, "region", "Page list"), "North").click()
        expect(title).to_have_value("North")
        north_url = page.url
        control(page, "button", "Back to book").click()
        entry(control(page, "region", "Page list"), "South").click()
        expect(title).to_have_value("South")
        expect(body).to_have_value("South observations")
        # Equivalent to selecting North in the browser's Back history menu.
        # Wait for North's response so stale fields cannot be a loading artifact.
        north_id = north_url.rsplit("/", 1)[-1]
        with page.expect_response(lambda r: r.url.endswith(f"/api/pages/{north_id}") and r.ok) as loaded:
            page.evaluate("history.go(-2)")
        loaded.value.finished()
        expect(page).to_have_url(north_url)
        expect(title).to_have_value("North")
        expect(body).to_have_value("North observations")

    def test_new_shelf_is_separate_from_bootstrap(self):
        page = self.page
        page.goto("/")
        name = "Benchmark Bootstrap Shelf"
        shelf_list = control(page, "region", "Shelf list")
        control(page, "link", "Shelves").click()
        entry(shelf_list, name).click()
        expect(control(page, "heading", name)).to_be_visible()
        seed_url = page.url
        control(page, "button", "New Shelf").click()
        control(page, "textbox", "Name").fill(name)
        control(page, "textbox", "Description").fill("Entry shelf for the New Shelf creation action.")
        with page.expect_response(
            lambda response: response.url.endswith("/api/shelves") and response.request.method == "POST"
        ) as save:
            control(page, "button", "Save Shelf").click()
        if save.value.status in (400, 409, 422):
            self.skipTest(f"The server declined creation (HTTP {save.value.status}).")
        self.assertTrue(save.value.ok, f"Unexpected shelf creation response: HTTP {save.value.status}")
        expect(shelf_list).to_be_visible()
        # Count business identities after the successful return to the list.
        # The immutable seed was present before this save.
        matches = entry(shelf_list, name)
        targets = set()
        for index in range(matches.count()):
            matches.nth(index).click()
            expect(control(page, "heading", name)).to_be_visible()
            targets.add(page.url)
            control(page, "link", "Shelves").click()
            expect(shelf_list).to_be_visible()
        self.assertIn(seed_url, targets)
        self.assertEqual(len(targets), 2, f"Successful save left these distinct shelf URLs: {targets}")

    def test_draft_edit_keeps_favorite_removable(self):
        page = self.page
        login(page)
        create_book(page, "Navigation manual")
        control(page, "button", "New Page").click()
        control(page, "textbox", "Page title").fill("Beacon signals")
        control(page, "textbox", "Write your page content here...").fill("Published v1")
        control(page, "button", "Save Page").click()
        entry(control(page, "region", "Page list"), "Beacon signals").click()
        expect(control(page, "heading", "Beacon signals")).to_be_visible()
        published_url = page.url

        control(page, "button", "Favorite").click()
        expect(control(page, "button", "Unfavorite")).to_have_attribute("aria-pressed", "true")
        page.goto("/")
        favorites_panel = control(page, "region", "My Most Viewed Favorites")
        favorite = entry(favorites_panel, "Beacon signals")
        expect(entry(control(page, "region", "Recently Updated Pages"), "Beacon signals")).to_be_visible()
        favorite.click()
        expect(page).to_have_url(published_url)
        control(page, "button", "Edit").click()
        expect(control(page, "textbox", "Page title")).to_have_value("Beacon signals")
        if control(page, "button", "Save Draft").count() == 0:
            self.skipTest("Editor does not expose Save Draft when editing an already-published page.")
        control(page, "textbox", "Write your page content here...").fill("Draft v2")
        with page.expect_response(lambda r: r.request.method in ("PUT", "POST") and "/pages" in r.url) as save:
            control(page, "button", "Save Draft").click()
        self.assertTrue(save.value.ok, f"Save Draft returned HTTP {save.value.status}")

        page.goto("/")
        expect(favorite).to_be_visible()
        favorite.click()
        unfavorite = control(page, "button", "Unfavorite")
        expect(unfavorite, "The page opened from favorites must let the user remove it.").to_be_visible()
        unfavorite.click()
        expect(control(page, "button", "Favorite")).to_have_attribute("aria-pressed", "false")
        page.goto("/")
        expect(favorites_panel).to_be_visible()
        expect(favorite).to_have_count(0)

    def test_bootstrap_shelf_remains_immutable(self):
        page = self.page
        page.goto("/")
        control(page, "link", "Shelves").click()
        entry(control(page, "region", "Shelf list"), "Benchmark Bootstrap Shelf").click()
        expect(control(page, "heading", "Benchmark Bootstrap Shelf")).to_be_visible()
        self.assertEqual(control(page, "button", "Edit").count(), 0)
        self.assertEqual(control(page, "button", "Delete").count(), 0)

        create_btn = entry(page, "Create New Book")
        if create_btn.count() == 0:
            return
        create_btn.click()
        control(page, "textbox", "Name").fill("Intruder volume")
        control(page, "textbox", "Description").fill("Added directly to bootstrap shelf")
        with page.expect_response(
            lambda r: "/api/" in r.url and r.request.method == "POST"
        ) as save:
            control(page, "button", "Save Book").click()
        if save.value.status in (400, 403, 409, 422):
            control(page, "link", "Shelves").click()
            entry(control(page, "region", "Shelf list"), "Benchmark Bootstrap Shelf").click()
            expect(control(page, "heading", "Benchmark Bootstrap Shelf")).to_be_visible()
            expect(entry(control(page, "region", "Book list"), "Intruder volume")).to_have_count(0)
            return

        expect(control(page, "heading", "Intruder volume")).to_be_visible()
        entry(page, "Benchmark Bootstrap Shelf").click()
        page.reload()
        expect(control(page, "heading", "Benchmark Bootstrap Shelf")).to_be_visible()
        count = entry(control(page, "region", "Book list"), "Intruder volume").count()
        self.assertEqual(
            count,
            0,
            f"Immutable bootstrap shelf now lists {count} user-created book(s) while Edit/Delete remain hidden.",
        )

    def test_anonymous_page_publish_matches_authenticated_creation(self):
        page = self.page

        def publish_twice(book_name):
            create_book(page, book_name)
            ids = []
            for _ in range(2):
                control(page, "button", "New Page").click()
                control(page, "textbox", "Page title").fill("Shift report")
                control(page, "textbox", "Write your page content here...").fill("All clear.")
                with page.expect_response(
                    lambda r: r.url.endswith("/pages") and r.request.method == "POST"
                ) as resp:
                    control(page, "button", "Save Page").click()
                self.assertTrue(resp.value.ok, f"Unexpected Save Page response: HTTP {resp.value.status}")
                ids.append(resp.value.json()["id"])
                expect(entry(control(page, "region", "Page list"), "Shift report").first).to_be_visible()
            return entry(control(page, "region", "Page list"), "Shift report").count(), ids

        page.goto("/")
        anon_count, anon_ids = publish_twice("Anonymous log")
        login(page)
        auth_count, auth_ids = publish_twice("Signed-in log")
        for state, count, ids in [("logged out", anon_count, anon_ids), ("signed in", auth_count, auth_ids)]:
            with self.subTest(login_state=state):
                self.assertEqual((count, len(set(ids))), (2, 2), f"{state}: {count} entries, page IDs {ids}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
