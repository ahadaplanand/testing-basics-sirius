from selenium import webdriver


driver = webdriver.Chrome(executable_path='/home/vealniycahko/Study/Testing/Bavykin/Test Project/2two/chromedriver')

driver.get(url='http://31.31.203.230')

login_page = driver.find_element_by_xpath(xpath='//*[@href="/api-auth/login/?next=/"]')
login_page.click()

username_field = driver.find_element_by_xpath(xpath='//*[@name="username"]')
username_field.send_keys('velichko_ivan')

password_field = driver.find_element_by_xpath(xpath='//*[@name="password"]')
password_field.send_keys('Asdq123455')

submit_button = driver.find_element_by_xpath(xpath='//*[@name="submit"]')
submit_button.click()

whoami = driver.find_element_by_xpath(xpath='//*[@class="dropdown-toggle"]')
assert whoami.text == 'velichko_ivan'
