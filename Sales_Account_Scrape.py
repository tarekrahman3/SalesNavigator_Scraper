import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
options = uc.ChromeOptions()
options.user_data_dir = "chrome_profile"
driver = uc.Chrome(options=options)

def scroll(driver):
	for i in range(5):
		driver.execute_script('window.scrollBy(0,window.innerHeight)')
		time.sleep(2)
	for i in range(5):
		driver.execute_script('window.scrollBy(0,-window.innerHeight)')
		time.sleep(2)
	for i in range(5):
		driver.execute_script('window.scrollBy(0,window.innerHeight)')
		time.sleep(2)
def get_name(driver, name_id):
	return driver.execute_script(f"return document.getElementById('{name_id}').innerText")


driver.get('https://linkedin.com')
driver.get(input('Sales Search URl'))
time.sleep(5)
d =[]
try:
	i = 0
	while i<37:
		scroll(driver)
		time.sleep(2)
		companys = driver.find_elements_by_xpath('//ol[@class="search-results__result-list"]/li')
		for each_person in companys:
			id = each_person.find_element_by_xpath('.//section[@class="result-lockup relative"]//dt//a').get_attribute('id')
			c_name = get_name(driver, id)
			c_url = each_person.find_element_by_xpath('.//*[@class="result-lockup__name"]/a').get_attribute('href')
			data = {
			'name':c_name,
			'c_url':c_url
			}
			print(f'{len(d)} | {c_name}')
			d.append(data)
		try:
			driver.execute_script("document.getElementsByClassName('search-results__pagination-next-button')[0].click()")
			time.sleep(5)
			driver.refresh()
			time.sleep(5)
		except:
			break
		i+=1
finally:
	pd.DataFrame(d).to_csv('export.csv',index=False)