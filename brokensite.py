from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from ping3 import ping
import os
import time
from datetime import datetime
from checkwebsite import checkwebsite


option = webdriver.ChromeOptions()
option.add_argument("--headless")
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-sh-usage")
# Start the chrome driver
driver = webdriver.Chrome(options=option)


def brokensite():
    urls_index = ["anime", "hentai", "manga"]
    working = 0
    not_working = 0
    false_positive = 0
    for index, library in enumerate(urls_index):
        # Start reading all the links from the file
        with open(f"{library}.txt", "r") as reader:
            for line in reader.readlines():
                print(f"Analyzing: {line}")
                url = "https://www.isitdownrightnow.com/{}.html".format(line.strip())

                driver.set_page_load_timeout(6)
                try:
                    driver.get(url)
                except TimeoutException as e:
                    continue

                # catch the updated html
                html = driver.page_source

                soup = BeautifulSoup(html, "lxml")
                time.sleep(3)
                try:
                    site_status = (
                        WebDriverWait(driver, 10)
                        .until(
                            EC.visibility_of_element_located(
                                (
                                    By.XPATH,
                                    "/html/body/div[2]/div[2]/div[1]/div[3]/div[5]/div",
                                )
                            )
                        )
                        .text
                    )
                except Exception as e:
                    site_status = "troll"
                    print("Not found, reading the title...")
                    title = soup.find("title").get_text()

                # If the website is UP
                if "UP and reachable by us" in site_status:
                    try:
                        status_text, site_name, url_checked, response_time, last_down = checkwebsite(driver, site_status, soup)
                        with open(f"websites_up_{library}.txt", "a") as writer:
                            writer.write(f"Site: {site_name}\n")
                            writer.write(f"URL: {url_checked}\n")
                            writer.write(f"Response Time: {response_time}\n")
                            writer.write(f"Last Down: {last_down}\n")
                            writer.write(f"Status: {status_text}\n")
                            writer.write("-------------------------------------------------\n")

                        print("The file was created successfully!")
                        # If the site is up, add +1 to the counter
                        working += 1
                    except Exception as e:
                        print("Error: ", e)

                # If the website is DOWN
                elif "is declined" in site_status or "DOWN for everyone" in site_status:
                    try:
                        status_text, site_name, url_checked, response_time, last_down = checkwebsite(driver, site_status, soup)
                        with open(f"website_down_{library}.txt", "a") as writer:
                            writer.write(f"Site: {site_name}\n")
                            writer.write(f"URL: {url_checked}\n")
                            writer.write(f"Response Time: {response_time}\n")
                            writer.write(f"Last Down: {last_down}\n")
                            writer.write(f"Status: {status_text}\n")
                            writer.write(f"{'-' * 49}\n")

                        print("The file was created successfully!")

                        # If the site is down, add +1 to the counter
                        not_working += 1
                    except Exception as e:
                        print("Error: ", e)
                # if the isitdownrightnow.com is broken or website is not valid
                elif title == "Is It Down Right Now - 404 Not Found" or "Enter a domain below" in title:
                    try:
                        hostname = line.strip()
                        # Ping the website
                        response_time = ping(hostname)

                        if response_time is not None:
                            status = "UP"
                            working += 1
                        else:
                            status = "DOWN"
                            not_working += 1

                        result = f"{hostname} is {status}"

                        with open(f"websites_tested_with_ping_{library}.txt", "a") as writer:
                            writer.write(f"URL: {hostname}\n")
                            writer.write(f"Status: {result}\n")
                            writer.write("-------------------------------------------------\n")
                        print("Added to the file!")
                    except Exception as e:
                        print("Error: ", e)
                # if the URL is invalid
                else:
                    with open("urls_ignored.txt", "a") as writer:
                        writer.write(f"URL: {line.strip()}\n")
                        writer.write("This URL is invalid or cannot be checked\n")
                        writer.write("-------------------------------------------------\n")
                        # If the site is invalid or cloudflare problem, add +1 to the counter
                        false_positive += 1

                # close the driver, clean the console and show the result

                if index < len(urls_index) - 1:
                    print(f"Current library: {library}")
                    time.sleep(2)
                elif reader.tell() == reader.seek(0, 2):
                    os.system("cls")
                    with open(
                        f"log_{library}_{datetime.now().strftime('%Y-%m-%d_%H')}.txt",
                        "a",
                    ) as writer:
                        writer.write(
                            f"Working: {working}\n" f"Not Working: {not_working}\n" f"False Positive: {false_positive}"
                        )
                    working, not_working, false_positive = 0, 0, 0
                else:
                    driver.quit()
                    print("All websites analysed, closing the driver...")


brokensite()

