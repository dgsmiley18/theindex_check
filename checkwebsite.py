from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def checkwebsite(driver, site_status, soup):
    try:
        status_text = site_status
        site_name = soup.select_one("div.tabletr:nth-child(1) > span:nth-child(1)").get_text()
        url_checked = soup.select_one("div.tabletrsimple:nth-child(2) > span:nth-child(1)").get_text()
        response_time = (
            WebDriverWait(driver, 1)
            .until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div[2]/div[1]/div[3]/div[3]/span",
                    )
                )
            )
            .text
        )
        last_down = (
            WebDriverWait(driver, 1)
            .until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div[2]/div[1]/div[3]/div[4]/span",
                    )
                )
            )
            .text
        )
        return status_text, site_name, url_checked, response_time, last_down
    except Exception as e:
        return print("Error: ", e)