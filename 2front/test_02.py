from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from json import loads


snippet_data = '''{
    "title": "Titlednbfjdbhdbfhdbf",
    "code": "Contentfjggjhjdngjdn contentosqosoqsoqsoqs contentjwnqimomsxxncjejeneend",
    "linenos": false,
    "language": "text",
    "style": "monokai"
}'''

driver = webdriver.Chrome(executable_path='/home/vealniycahko/Study/Testing/Bavykin/Test Project/2two/chromedriver')
driver.get(url='http://31.31.203.230')


# Authorization
driver.find_element(by=By.XPATH, value='//*[@href="/api-auth/login/?next=/"]').click()
driver.find_element(by=By.XPATH, value='//*[@name="username"]').send_keys('velichko_ivan')
driver.find_element(by=By.XPATH, value='//*[@name="password"]').send_keys('Asdq123455')
driver.find_element(by=By.XPATH, value='//*[@name="submit"]').click()


# Check authorization
whoami = driver.find_element(by=By.XPATH, value='//*[@class="dropdown-toggle"]')
assert whoami.text == 'velichko_ivan', 'You are not logged in to your account, or it is incorrect...'


# Create snippet
driver.find_element(by=By.XPATH, value='//*[@href="http://31.31.203.230/snippets/"]').click()
driver.find_element(by=By.XPATH, value='//*[@name="raw-tab"]').click()

json_field = driver.find_element(by=By.XPATH, value='//*[@name="_content"]')
json_field.clear()
json_field.send_keys(snippet_data)

driver.find_element(by=By.XPATH, value='//*[@id="post-generic-content-form"]/form/fieldset/div[3]/button').click()
sleep(1)

content_field = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[4]/pre')
var = content_field.text
json_content = var[var.find('{'):]
snippet_id = loads(json_content)['id']


# Find snippet
driver.find_element(by=By.XPATH, value='//*[@href="/snippets/"]').click()
driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/nav/ul/li[6]/a').click()

flag = True
while flag:
    content_field = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[4]/pre')
    var = content_field.text
    json_content = var[var.find('{'):]

    for i in loads(json_content)['results']:
        if i['id'] == snippet_id:
            snippet_url = i['url']
            driver.find_element(by=By.LINK_TEXT, value=snippet_url).click()
            flag = False
            break

    if flag:
        try:
            driver.find_element(by=By.XPATH, value=f'//*[@id="content"]/div[2]/div[4]/pre/a[1]/span').click()
        except NoSuchElementException:
            break
assert not flag, 'Snippet not found...'


# Delete snippet
driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/button').click()
sleep(1)
driver.find_element(by=By.XPATH, value='//*[@id="deleteModal"]/div/div/div[2]/form/button').click()
sleep(1)


# Check deletion
driver.find_element(by=By.XPATH, value='//*[@href="/snippets/"]').click()
flag = True
while flag:
    content_field = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[4]/pre')
    var = content_field.text
    json_content = var[var.find('{'):]

    for i in loads(json_content)['results']:
        if i['id'] == snippet_id:
            flag = False
            break

    if flag:
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[4]/pre/a[1]/span').click()
        except NoSuchElementException:
            break
assert flag, 'Snippet not deleted...'


# Log out
driver.get(url='http://31.31.203.230')
driver.find_element(by=By.XPATH, value=f'//*[@href="#"]').click()
driver.find_element(by=By.XPATH, value=f'//*[@href="/api-auth/logout/?next=/"]').click()
