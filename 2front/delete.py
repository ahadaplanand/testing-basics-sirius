from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from json import loads


driver = webdriver.Chrome(executable_path='/home/vealniycahko/Study/Testing/Bavykin/Test Project/2two/chromedriver')
driver.get(url='http://31.31.203.230')

# Authorization
driver.find_element(by=By.XPATH, value='//*[@href="/api-auth/login/?next=/"]').click()
driver.find_element(by=By.XPATH, value='//*[@name="username"]').send_keys('velichko_ivan')
driver.find_element(by=By.XPATH, value='//*[@name="password"]').send_keys('Asdq123455')
driver.find_element(by=By.XPATH, value='//*[@name="submit"]').click()

# Get snippets list
driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[4]/pre/a[3]/span').click()
content_field = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[4]/pre')
var = content_field.text
json_content = var[var.find('{'):]
my_snippets = loads(json_content)['results'][0]['snippets']

# Go to snippets
driver.find_element(by=By.XPATH, value=f'//*[@href="/"]').click()
driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[4]/pre/a[2]/span').click()

# Delete snippets
flag = True
page = 2
while flag:
    content_field = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[4]/pre')
    var = content_field.text
    json_content = var[var.find('{'):]

    for i in loads(json_content)['results']:
        if i['url'] in my_snippets:
            snippet_url = i['url']
            driver.find_element(by=By.LINK_TEXT, value=snippet_url).click()
            driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/button').click()
            sleep(1)
            driver.find_element(by=By.XPATH, value='//*[@id="deleteModal"]/div/div/div[2]/form/button').click()
            sleep(1)
            driver.back()

    try:
        driver.find_element(by=By.XPATH, value=f'//*[@href="http://31.31.203.230/snippets/?page={page}"]').click()
    except NoSuchElementException:
        break
    page += 1

# После удаления часто происходит лажа
