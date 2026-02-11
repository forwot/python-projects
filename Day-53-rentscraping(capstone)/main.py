from bs4 import BeautifulSoup
import requests
import re

url = "https://appbrewery.github.io/Zillow-Clone/"
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
          "Accept_Language": "en-US"
        }

response = requests.get(url, headers=header)
soup = BeautifulSoup(response.content, "html.parser")

rent_data = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
rent_prices = [rent.text for rent in rent_data]

final_rent = []
pattern = r'(\$[\d,]+)'
for item in rent_prices:
    # Search for the pattern in the string
    match = re.search(pattern, item)
    # If a match is found
    if match:
        # Get the part inside the parentheses (group 1)
        price_str = match.group(1)
        final_rent.append(price_str)

address_data = soup.find_all("address")
addresses = [address.text.strip() for address in address_data]

anchor_tags = soup.find_all(class_="StyledPropertyCardDataArea-anchor")
link_list = []
for a in anchor_tags:
    href = a.get("href")
    link_list.append(href)

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://docs.google.com/forms/d/e/1FAIpQLSesmDslGmmNPXyr6u3rviUT1p3ZinIYldSRzdvidPLN9WJpeA/viewform?usp=header")
sleep(2)

for x in range(len(final_rent)):
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(addresses[x])

    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(final_rent[x])

    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(link_list[x])

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    sleep(1)

    again_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    again_button.click()
    sleep(1)

driver.quit()