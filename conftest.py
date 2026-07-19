import pytest
from playwright.sync_api import sync_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg0NDQ3MDQ4LCJpYXQiOjE3ODQzOTgzMzcsImp0aSI6ImM0Y2Y2MzI1ZWQzMDQzMmViNWViYTA1OGZhOGQ2MWFmIiwidXNlcl9pZCI6MzUsImlzX3NzbyI6dHJ1ZSwic3NvX3Byb3ZpZGVyX3VzZXJfaWQiOiIzNjdiZDAzOC00YjkwLTQ0NzctYWI4OS1kYzhlY2JiNzgxNzkiLCJzc29fY2xpZW50X2lkIjoxLCJyZWZyZXNoX2p0aSI6IjliZDA2MzMzZjIyOTQ5NTM5MDA2MzFhMjI1MmMyYjJmIn0.TqMAjvsk7I5pQZzblaNYq5PPLdoUzZKoY4ESo3mNHOE"
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4NDQ4NDczNywiaWF0IjoxNzg0Mzk4MzM3LCJqdGkiOiI5YmQwNjMzM2YyMjk0OTUzOTAwNjMxYTIyNTJjMmIyZiIsInVzZXJfaWQiOjM1LCJpc19zc28iOnRydWUsInNzb19wcm92aWRlcl91c2VyX2lkIjoiMzY3YmQwMzgtNGI5MC00NDc3LWFiODktZGM4ZWNiYjc4MTc5Iiwic3NvX2NsaWVudF9pZCI6MX0.sAcMeVGqmz5iVCLFmp3jG1QxcfMFb3taN1cr8bqoPkU"
@pytest.fixture(scope="session")
def authenticated_page():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)

        context = browser.new_context()
        page = context.new_page()

        page.goto("https://sentinel.oritiq.org/login")

        page.evaluate(
            """
            ([access, refresh]) => {
                localStorage.setItem("access_token", access);
                localStorage.setItem("refresh_token", refresh);
            }
            """,
            [ACCESS_TOKEN, REFRESH_TOKEN]
        )

    
        page.reload()

        yield page

        browser.close()
@pytest.fixture
def test_data():
    return {}


@pytest.fixture(autouse=True)
def reload_after_scenario(authenticated_page):
    """Reload the authenticated page after each test/scenario to ensure clean state."""
    yield
    try:
        authenticated_page.reload()
        authenticated_page.wait_for_load_state("networkidle")
    except Exception:
        # best-effort reload; don't fail the test because of reload errors
        pass
