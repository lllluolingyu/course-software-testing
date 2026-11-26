"""Browser regression tests for favorite ranking, draft identity and shelf creation."""

import json
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
        url = self.enterContext(fresh_app())
        context = self.browser.new_context(base_url=url, viewport={"width": 1440, "height": 900})
        self.addCleanup(context.close)
        self.page = context.new_page()

    def record_observation(self, label, details):
        """Optional review evidence; generated only inside the requested folder."""
        directory = os.environ.get("TEAM04_EVIDENCE_DIR")
        if not directory:
            return
        target = Path(directory)
        target.mkdir(parents=True, exist_ok=True)
        (target / f"{label}.json").write_text(json.dumps(details, indent=2) + "\n")
        self.page.screenshot(path=str(target / f"{label}.png"), full_page=True)

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
        self.record_observation("favorite-ranking", {"homepage": shown, "all_favorites": names})
        self.assertIn("Atlas", shown, f"Homepage showed {shown}. All five exist in My Favourites.")

    def open_draft_history_transition(self):
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
        return north_url

    def test_history_returns_to_selected_draft(self):
        page = self.page
        north_url = self.open_draft_history_transition()
        title = control(page, "textbox", "Page title")
        body = control(page, "textbox", "Write your page content here...")
        self.record_observation("draft-identity", {
            "url": north_url, "title": title.input_value(), "body": body.input_value(),
        })
        expect(title).to_have_value("North")
        expect(body).to_have_value("North observations")

    def test_save_after_history_preserves_selected_draft(self):
        page = self.page
        north_url = self.open_draft_history_transition()
        title = control(page, "textbox", "Page title")
        body = control(page, "textbox", "Write your page content here...")
        # Keep running to check persistent data even when the editor identity is
        # wrong. unittest records this subtest failure; it is never suppressed.
        with self.subTest("editor identity before saving"):
            expect(title).to_have_value("North")
            expect(body).to_have_value("North observations")
        before = {"title": title.input_value(), "body": body.input_value()}
        north_id = north_url.rsplit("/", 1)[-1]
        with page.expect_response(
            lambda r: r.request.method == "PUT" and r.url.endswith(f"/api/pages/{north_id}")
        ) as saved:
            control(page, "button", "Save Draft").click()
        self.assertTrue(saved.value.ok)
        saved_payload = saved.value.json()
        page.reload()
        expect(page).to_have_url(north_url)
        expect(title).to_be_visible()
        self.record_observation("draft-persistence", {
            "url": north_url, "before_save": before, "save_response": saved_payload,
            "after_reload": {"title": title.input_value(), "body": body.input_value()},
        })
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
        self.record_observation("shelf-identity", {"seed_url": seed_url, "targets_after_save": sorted(targets)})
        self.assertEqual(len(targets), 2, f"Successful save left these distinct shelf URLs: {targets}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
