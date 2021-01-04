import numpy as np
import os
from selenium.webdriver.common.by import By
from selenium import webdriver

try:
	os.mkdir("chems")
except:
	pass
driver = webdriver.Chrome()

chems = []
broken = False
for name in os.listdir("urls"):
	urls = np.load("urls/" + name)
	gots = int(name.replace("urls", "").replace(".npy", ""))

	for url in urls:
		driver.get(str(url))
		try:
			chem = driver.find_element(By.XPATH, '//*[contains(text(), "SMILE")]')
			chem = str(chem.find_element_by_xpath('//td[2]').text)
		except:
			print("breaker: ", url)
			broken = True
			break
		chems.append(chem)

	if broken:
		continue

	np.save("chems/chems" + str(gots) + ".npy", np.array(chems))