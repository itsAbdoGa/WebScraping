import json
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

# note : be sure to run fixer.py before running this
query = "data scraping"
url = f"https://www.linkedin.com/search/results/content/?keywords={query}&sortBy=%22date_posted%22"

def main():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()


        with open('cookies_fixed.json', 'r') as file:
            cookie = json.load(file)

        context.add_cookies(cookies=cookie)

        # Open a new page and navigate to the website
        page = context.new_page()
        page.set_default_navigation_timeout(120000)

        page.goto(url)
        return page.content()

def parse(content):
    parsed = HTMLParser(content)
    print(f"PARSED CONTENT :{parsed}")
    posts = parsed.css("li[class='artdeco-card mb2']")
    print(f"PARSED POSTS:{len(posts)}")
    for post in posts:
        data = []
        name = post.css_first("a[class*='update-components-actor__meta'] span[class*='actor__title'] span[aria-hidden='true']")
        if name:
            name = name.text().strip()
            data.append({"name":name})
        job = post.css_first("a[class*='update-components-actor__meta'] span[class*='actor__description'] span[aria-hidden='true']")
        if job:
            job = job.text().strip()
            data.append({"job":job})
        desc_element = post.css_first("div.update-components-text.relative.update-components-update-v2__commentary > span > span[dir='ltr']")
        if desc_element:
            desc = desc_element.text().strip()
            data.append({"desc":desc})
            print(data)
parse(main())