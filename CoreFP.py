from os import popen, system
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gpiozero import Button

PortalUserName =''
PortalPassword =''
NOAA           ='https://w1.weather.gov/obhistory/KHOU.html'

# Start Plotting
system('python3 /home/pi/Desktop/FlightProfilePlotter.py &')

# Click once available without having to sleep
def WaitThenClick(ThisXPath):
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH,ThisXPath)))
    driver.find_element_by_xpath(ThisXPath).click()

# Shutting down
def StopRecording():
    # Stop recording
    WaitThenClick("//*[@id='root']/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/button[2]")
    WaitThenClick("/html/body/div[2]/div/div/div/form/div[2]/button[1]")
    # Stop tracking
    WaitThenClick("//*[@id='root']/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/button[1]")
    system('sudo poweroff')
StopRecording_btn = Button(4, hold_time=2)
StopRecording_btn.when_held = StopRecording

# Find the location of driver
chrome_path = popen('dpkg -L chromium-chromedriver|grep /chromedriver').read().replace('\n','')
# Hide Chrome
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# Launch browser
driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_options)
# Get Pressure and Temprature from NOAA
driver.get(NOAA)
P=int(float(driver.find_element_by_xpath('/html/body/table[4]/tbody/tr[4]/td[15]').text)*100)
T=int(driver.find_element_by_xpath('/html/body/table[4]/tbody/tr[4]/td[7]').text)
# Go to login page
driver.get('https://spa.brainium.com/login')
# Enter email
driver.find_element_by_name("email").send_keys(PortalUserName)
# Enter password
driver.find_element_by_name("password").send_keys(PortalPassword)
# Click login
WaitThenClick("//*[@id='root']/div/div/div[1]/form/button")
# Wait for project to come up then click it
WaitThenClick("//*[@id='root']/div[2]/div/div/div[2]/div[1]/div/div/div/a")
# Wait for button to show up
ThisXPath="//*[@id='root']/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/button"
WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH,ThisXPath)))
# Start tracking
if driver.find_element_by_xpath(ThisXPath+"/div/span").text == "Start Tracking":
    driver.find_element_by_xpath(ThisXPath).click()
    # Start as is
    WaitThenClick("//*[@id='fullscreen-modal-container']/div/div/div/div[5]/div/div/button")
# Start recording
ThisXPath='//*[@id="root"]/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/button[2]'
while not (driver.find_element_by_xpath(ThisXPath).is_enabled()):pass
WaitThenClick(ThisXPath)
# MQTT connection
system('python3 /home/pi/Desktop/MQTTFP.py {P} {T}'.format(P=P,T=T))



