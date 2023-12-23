#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from pyvirtualdisplay import Display

import argparse

parser = argparse.ArgumentParser(description="Run the script locally or not")
parser.add_argument(
    "--local", dest="run_locally", action="store_true", help="Run the script locally"
)

args = parser.parse_args()

urls = ["https://tttc-turbo.web.app", "http://localhost:5173"]

url = urls[args.run_locally]

display = Display(visible=0, size=(800, 800))
display.start()

chromedriver_autoinstaller.install()

chrome_options = webdriver.ChromeOptions()
options = ["--window-size=1200,1200", "--ignore-certificate-errors"]

for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(options=chrome_options)


def test_report(name):
    driver.get(f"{url}/report/{name}")
    WebDriverWait(driver, 60).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Show more")
    )
    print(f"Testing: {name}")
    assert "Show more" in driver.page_source
    assert "Subtopics" in driver.page_source
    assert "Claims" in driver.page_source
    assert "Quote" in driver.page_source
    assert "AI Objectives Institute" in driver.page_source
    assert "Home" in driver.page_source
    assert "About" in driver.page_source
    assert "Sign in" in driver.page_source
    assert "Fork Report" in driver.page_source


tests = ["mina-protocol", "heal-michigan-9", "taiwan-zh", "台灣初步測試"]

for test in tests:
    test_report(test)

driver.close()