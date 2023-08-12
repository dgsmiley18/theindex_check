import io
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from PIL import Image
from urllib.parse import urlparse
import time

logging.basicConfig(level=logging.ERROR)
option = webdriver.ChromeOptions()
option.add_argument("--headless")
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-sh-usage")
# Setup selenium to use a chrome
driver = webdriver.Chrome(options=option)

# Load the page with selenium
driver.get("https://theindex.moe/library/anime")
time.sleep(2)
# Get the complete HTML from the page
select_element = Select(
    driver.find_element(By.CSS_SELECTOR, "select.Input_input___QkW_:nth-child(1)")
)
select_element.select_by_index(3)
time.sleep(10)

# Get the width and height of the page (Page does not loads completely)
width = driver.execute_script(
    "return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth, document.body.offsetWidth, document.documentElement.offsetWidth, document.documentElement.clientWidth);"
)
height = driver.execute_script(
    "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight, document.documentElement.clientHeight);"
)

# Set browser window dimensions to span the entire page (so it can scrape all the links)
driver.set_window_size(width, height)

# Take a full screenshot
screenshot = driver.get_screenshot_as_png()

# Take a screenshoot with PIL
image = Image.open(io.BytesIO(screenshot))

image.save("screenshot.png")

# Update the HTML with the new HTML
html = driver.execute_script("return document.documentElement.outerHTML")
# Close the selenium for save resources
driver.quit()

# Give the HTML to BS for analyse
soup = BeautifulSoup(html, "html.parser")
count = 0
divs = soup.find("div", class_="d-flex flex-wrap my-2").find_all(
    "div", class_="Card_card__pf4Rb card bg-2 mb-2 me-2"
)

# Starts to browse all registered websites

for div in divs:
    count += 1
    try:
        with open("links.txt", "a") as writer:
            link = (
                div.find("div", class_="row g-0 h-100")
                .find("div", class_="card-body d-flex flex-column p-2 h-100")
                .find("h5", class_="Card_title__6erSA card-title")
                .find("a")
                .get("href")
            )

            # if the link is not github.com, parse the url to remove https and /
            # Example: itazuraneko.neocities.org
            if "github.com" not in link:
                parsed_url = urlparse(link)
                site_link = parsed_url.netloc
                if site_link.startswith("www."):
                    site_link = site_link[4:]
                writer.write(site_link + "\n")
                continue

            link = link.replace("https://", "")
            link = link.replace("http://", "")
            link = link.replace("www.", "")

            if link.endswith("/"):
                link = link[:-1]
            writer.write(link + "\n")
        print("New link added to links.txt!")
    except Exception as e:
        print("Error: ", e)

print(f"Websites found on TheIndex: {count}")
