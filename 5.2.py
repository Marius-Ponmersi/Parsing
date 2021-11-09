from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
import time
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import re


client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
trend = db.trend

options = Options()
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(executable_path=r'F:\Vadim\GeekBrains\2_semestre\Methods_of_collecting_and_processing_data_from_the_Internet\Parsing\chromedriver.exe',
                          options=options)
driver.implicitly_wait(10)

url = 'https://www.mvideo.ru/'
driver.get(url)
actions = ActionChains(driver)
actions.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN)
actions.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN)
actions.perform()

button = driver.find_element(By.XPATH, "//div[@class = 'mvid-carousel-inner']/button[2]/div")
button.click()

# button = driver.find_element(By.XPATH, "//mvid-carousel[contains(@class, 'carusel')]//button[contains(@class, 'forward')]/mvid-icon")
# button.click()
while True:
    try:
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//mvid-carousel[contains(@class, 'carusel')]//button[contains(@class, 'forward')]/mvid-icon")))
        button.click()
    except (ElementNotInteractableException, TimeoutException):
        break


# link = driver.find_element(By.XPATH, "//mvid-carousel[contains(@class, 'carusel')]//a/img/..").get_attribute('href')
# driver.execute_script(f'''window.open("{link}", "_blank");''')
# driver.switch_to.window(driver.window_handles[1])
# name = driver.find_element(By.XPATH, "//h1[@class='title']").text
# try:
#     price = driver.find_element(By.XPATH, "//mvid-price//span[@class='price__main-value']").text
#     price = price.replace(" ", "")
#     price = re.findall(r'\d+', price)
#     price = float(price[0])
# except:
#     price = None
# link = link
# _id = link
# print(name, price, link)

links = driver.find_elements(By.XPATH, "//mvid-carousel[contains(@class, 'carusel')]//a/img/..")

for link in links:
    link = link.get_attribute('href')
    driver.execute_script(f'''window.open("{link}", "_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    product_data = {}
    name = driver.find_element(By.XPATH, "//h1[@class='title']").text
    try:
        price = driver.find_element(By.XPATH, "//mvid-price//span[@class='price__main-value']").text
        price = price.replace(" ", "")
        price = re.findall(r'\d+', price)
        price = float(price[0])
    except:
        price = None
    
    product_data['name'] = name
    product_data['price'] = price
    product_data['link'] = link
    product_data['_id'] = link

    try:
        trend.insert_one(product_data)
    except dke:
        print(f"Документ с id = {product_data['_id']} уже существует в базе")

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.quit()
