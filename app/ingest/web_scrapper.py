import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_url_async(url: str):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)  # or chromium/webkit
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        # get rendered HTML
        content = await page.content()
        await browser.close()

    # parse with BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # extract text content (simplified)
    text = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])
    metadata = {
        "title": soup.title.string if soup.title else None,
        "url": url,
        "length": len(text)
    }
    return text, metadata


def scrape_url(url: str):
    """Sync wrapper for convenience"""
    return asyncio.run(scrape_url_async(url))
