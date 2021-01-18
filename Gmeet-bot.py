from logging import log
from platform import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import  time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.webdriver import WebDriver
import schedule
import getpass
import sys

PATH = "chromedriver.exe"
login_link = "https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin"

link_and_time = {}
class_timings = []
already_loggedin = False
#pre_time = time.ctime()[11:16]


print("""
		 ██████╗ ███╗   ███╗███████╗███████╗████████╗    ██████╗  ██████╗ ████████╗
		██╔════╝ ████╗ ████║██╔════╝██╔════╝╚══██╔══╝    ██╔══██╗██╔═══██╗╚══██╔══╝
		██║  ███╗██╔████╔██║█████╗  █████╗     ██║       ██████╔╝██║   ██║   ██║   
		██║   ██║██║╚██╔╝██║██╔══╝  ██╔══╝     ██║       ██╔══██╗██║   ██║   ██║   
		╚██████╔╝██║ ╚═╝ ██║███████╗███████╗   ██║       ██████╔╝╚██████╔╝   ██║   
		╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝   ╚═╝       ╚═════╝  ╚═════╝    ╚═╝   
																					
	""")




def classes():
  while True:
    try:
       classi = int(input("Enter number of classes:"))       
    except ValueError:
       print("Enter an integer(1-9)")
       continue
    else:
       return classi
       break 
class_number  = classes()
if class_number == 0:
	print("no classes today! Enjoy")
	sys.exit()
else:
	#credentials
	Email = input("Enter your mail id: ")
	passw = getpass.getpass(prompt='Enter your password: ') 
	
	for i in range(1, class_number+1):
		class_link = input("Enter classlink: ")
		class_time = input("Enter class time in 24hr format: ") 
		#class_links.append(class_link)
		class_timings.append(class_time)
		link_and_time[class_time] = class_link
		class_duration = input("Enter class duration in minutes(default is 60minutes): ")
		if len(class_duration) == 0:
			class_duration = 60

def Work():
	options = webdriver.ChromeOptions()
	options.add_argument("--disable-infobars")

	options.add_experimental_option("prefs", { \
		 "profile.default_content_setting_values.media_stream_mic": 1,     # 1:allow, 2:block
		 "profile.default_content_setting_values.media_stream_camera": 1,
		 "profile.default_content_setting_values.notifications": 2
		 })
	

	driver = webdriver.Chrome(PATH,  chrome_options=options)
	
#login to gmail
	def login(): 
		already_loggedin = True
		print("-------logging in gmail-----------------")
		driver.get(login_link)
		driver.find_element_by_name("identifier").send_keys(Email)
		time.sleep(1)

		try: 
			driver.find_element_by_id("identifierNext").click()
			time.sleep(4)
		except:
			driver.find_element_by_id("next").click()
			time.sleep(4)

		driver.find_element_by_name("password").send_keys(passw)
		time.sleep(1)

		try:    
			driver.find_element_by_id("passwordNext").click()
			time.sleep(4)
		except:   
			driver.find_element_by_id("trustDevice").click()
			driver.find_element_by_id("submit").click()
			time.sleep(4)
			print("---------------------successfully logged in gmail--------------------")
	#joining class
	def join_class():
		print("-------------------waiting to join class-----------------------")
		
		if time.ctime()[11:16] in link_and_time:
			driver.get(link_and_time[time.ctime()[11:16]])
		
		print("----------------joining class-----------------")
		time.sleep(6)
		element=driver.find_element_by_xpath("//body")
		#print(options.experimental_options)
		element.send_keys(Keys.CONTROL, 'd')
		element.send_keys(Keys.CONTROL, 'e')
		driver.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Join now')]").click()
		print("----------------------------joined class-------------------")
	#leave class
	def leave_class():
		print("--------------class running-----------")
		time.sleep(int(class_duration)*60)
		print("-----------------leaving class---------------")
		driver.find_element_by_xpath('//span[@class = "wnPUne N0PJ8e"]').click()
		button = driver.find_element_by_xpath('/html/body/div[1]/c-wiz/div[1]/div/div[8]/div[3]/div[9]/div[2]/div[2]/div/div[1]')
		driver.execute_script("arguments[0].click();", button)
		driver.close()
		print("--------------left class-------------")
		return schedule.cancel_job
	login()
	join_class()
	leave_class()
for i in class_timings:
	schedule.every().day.at(i).do(Work)
	
		
while True:
	schedule.run_pending()

