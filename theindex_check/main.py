import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse
import time
import brokensite


logging.basicConfig(level=logging.ERROR)
option = webdriver.ChromeOptions()
option.add_argument("--headless")
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-sh-usage")
# Setup selenium to use a chrome
driver = webdriver.Chrome(options=option)

urls_index = ["anime", "hentai", "manga", "novels"]

for index, library in enumerate(urls_index):
    # Load the page with selenium
    driver.get(f"https://theindex.moe/library/{library}")
    time.sleep(5)

    # Select the option (ALL) to show all the websites
    select_element = Select(
        driver.find_element(
            By.XPATH, "/html/body/div/div/div[1]/main/div[5]/div/select"
        )
    )
    select_element.select_by_index(3)
    time.sleep(3)

    # Get the width and height of the page (Page does not loads completely)
    width = driver.execute_script(
        "return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth, document.body.offsetWidth, document.documentElement.offsetWidth, document.documentElement.clientWidth);"
    )
    height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight, document.documentElement.clientHeight);"
    )

    # Set browser window dimensions to span the entire page (so it can scrape all the links)
    driver.set_window_size(width, height)

    # Update the HTML with the new HTML
    html = driver.execute_script("return document.documentElement.outerHTML")

    # Give the HTML to BS for analyse
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find("div", class_="d-flex flex-wrap my-2").find_all(
        "div", class_="Card_card__X0xjX card bg-2 mb-2 me-2"
    )

    # Starts to browse all registered websites
    count = 0

    for div in divs:
        count += 1
        try:
            with open(f"{library}.txt", "a") as writer:
                link = (
                    div.find("div", class_="row g-0 h-100")
                    .find("div", class_="card-body d-flex flex-column p-2 h-100")
                    .find("h5", class_="Card_title__8lWUm card-title")
                    .find("a")
                    .get("href")
                )
                # parse the url to remove https and /
                # Example: itazuraneko.neocities.org
                parsed_url = urlparse(link).netloc
                writer.write(parsed_url + "\n")

            print(f"{parsed_url} has been added to links.txt!")
        except Exception as e:
            print("Error: ", e)

    print(f"Websites found on TheIndex in the library {library}: {count}")

    if index < len(urls_index) - 1:
        next_library = urls_index[index + 1]
        print(f"Current library: {library}, Next library: {next_library}")
        print("Waiting 10 seconds before the next library")
        time.sleep(5)
    else:
        driver.quit()
        print("All websites collected, analysing them...")

brokensite()
