from selenium import webdriver
import BotEngine

#change selenium settings to stay open when session is terminated
from selenium.webdriver import ChromeOptions, Chrome
opts = ChromeOptions()
opts.add_experimental_option("detach", True)

chromedriver_path = '/Users/wesamazaizeh/Desktop/Projects/InstaBot/chromedriver'
webdriver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=opts)

BotEngine.init(webdriver)
BotEngine.update(webdriver)

webdriver.close()
