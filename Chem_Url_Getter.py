from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import get_links
import urllib
import numpy as np
import os
import time
from selenium import webdriver
import re
import pyautogui

try:
	os.mkdir("urls")
except:
	pass

options = webdriver.ChromeOptions()
options.add_argument("--width=1500")
driver = webdriver.Chrome(options=options)

def look_through(url, driver, ya):
	urls = []
	reset = 0

	EC_num = driver.title.split("EC ")[1]  #.get_attribute("title") #.split("EC ")[1]

	ecL = 'https://enzyme.expasy.org/EC/' + EC_num

	html = str(urllib.request.urlopen(ecL).read())
	try:
		html = html.split('<td colspan="2">')[1]
	except:
		raise IndexError
	html = html.split("</td>")[0]

	num = html.count("+") + 2  # also incudes reaction link for no reason

	driver.set_window_size(1550, 1080)

	text = driver.find_element(By.XPATH, '//*[contains(text(), "BioCyc ID:")]').text.split(": ")[1].replace("-", "_")
	end = 1500
	base = 25


	#amount = 0
	#c = 4
	y = 610 + ya

	list = len(re.findall("TAX\-", str(urllib.request.urlopen(url).read())))

	y += (list) * 27

	try:
		driver.find_element(By.XPATH, '//*[contains(text(), "In Pathway")]')
		y += 16
	except:
		pass

	if y > 1200:
		raise IndexError

	#driver.execute_script("arguments[0].value = 'foo.jpg';", driver.find_element_by_xpath('//*[@id="canvas-WG_SAMDECARB_RXN_REACTION_COLOR_div"]'))

	print(y)

	# make a for loop to scan across compound area and get every compound page by seeing breaks in "pointer state"
	# move like 15 px at a time mabye more?
	for interval in range(end // 15):
		pyautogui.moveTo(base + interval * 15, y, .0001)

		element = str(
			driver.find_element_by_xpath('//*[@id="canvas-WG_' + text + '_REACTION_COLOR_div"]').get_attribute('style'))
		if "pointer" not in element and reset == 0:
			pyautogui.moveTo(base + (interval - 1) * 15, y, .0001)
			pyautogui.click()
			if "id=PROTON" in str(driver.current_url):
				reset = 1
				driver.get(url)
			else:
				urls.append(driver.current_url)
				reset = 1
				driver.get(url)
		if "pointer" in element:
			reset = 0


	pyautogui.moveTo(140, 800, .0001)
	return num, urls



xpath = '//*[@id="popupNaN"]/div[2]'
gots = 0
alreadys = 0
for name in os.listdir("ec"):
	if alreadys != 0:
		alreadys -= 1
		continue
	ec = np.load("ec/" + name)
	url = str(ec[0][0])
	driver.get(url)

	gots += 1

	try:
		num, urls = look_through(url, driver, 0)
	except:
		continue

	urls.remove(url)

	print(urls)
	print(url)
	print(num)
	if len(urls) == num:
		np.save("urls/urls" + str(gots) + ".npy", np.array(urls))
	#else:
	#	print(num)
	#	print(url)
	print("gots: ", gots)

