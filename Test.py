from pyvirtualdisplay import Display
from selenium import webdriver
import os

# Set screen resolution to 1366 x 768 like most 15" laptops
display = Display(visible=0, size=(800, 500))
display.start()


path = os.path.dirname(os.path.abspath(__file__))
gecko_path = "/home/ubuntu/NIKE/gecko.exe"
  
# now Firefox will run in a virtual display.
browser = webdriver.Firefox(executable_path=gecko_path)

# Sets the width and height of the current window
browser.set_window_size(500, 400)

# Open the URL
browser.get('https://www.vionblog.com/')

# set timeouts
browser.set_script_timeout(30)
browser.set_page_load_timeout(30) # seconds

# Take screenshot
browser.save_screenshot('vionblog.png')

# quit browser
browser.quit()

# quit Xvfb display
display.stop()
