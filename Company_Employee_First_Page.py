import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
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
	#for i in range(5):
	#	driver.execute_script('window.scrollBy(0,window.innerHeight)')
	#	time.sleep(2)
def get_name(driver, name_id):
	return driver.execute_script(f"return document.getElementById('{name_id}').innerText")

d=[]
driver.get('https://linkedin.com')
input('Enter to Continue')
time.sleep(5)

companys = pd.read_csv('company_id_list.csv').company.tolist()

try:
	for Company_id in companys:
		driver.get(f'https://www.linkedin.com/sales/search/people/list/employees-for-account/{Company_id}')
		scroll(driver)
		time.sleep(2)
		persons = driver.find_elements_by_xpath('//ol[@class="search-results__result-list"]/li')
		n=[]
		for each_person in persons:
			name_id = each_person.find_element_by_xpath('.//section[@class="result-lockup"]//dt//a').get_attribute('id')
			name = get_name(driver, name_id)
			profile_url_ = each_person.find_element_by_xpath('.//*[@class="result-lockup__name"]/a').get_attribute('href')
			profile_url = re.sub(',.+','',profile_url_)
			try:
				title = each_person.find_element_by_xpath('.//span[@data-anonymize="job-title"]').text
			except:
				title = None
			try:
				company = each_person.find_element_by_xpath('.//span[@data-anonymize="company-name"]').text
			except:
				company = None
			data = {
			'name':name,
			'profile_url':profile_url,
			'title':title,
			'company':company
			}
			print(f'{len(d)} | {name} | {title} | {company}')
			n.append(data)
		d.append({'company_id':Company_id,'data':n})
finally:
	pd.DataFrame(d).to_csv('export.csv',index=False)