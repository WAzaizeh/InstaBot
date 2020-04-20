from selenium import webdriver
import Constants, BotEngine

# for Dev Mode
# # change selenium settings to stay open when session is terminated
# from selenium.webdriver import ChromeOptions, Chrome
# opts = ChromeOptions()
# opts.add_experimental_option("detach", True)
# webdriver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=opts)


# initialize Constants to get the settings from "settings.json"
Constants.init()

chromedriver_path = Constants.CHROME_DRIVER_PATH
webdriver = webdriver.Chrome(executable_path=chromedriver_path)

BotEngine.init(webdriver)
BotEngine.update(webdriver)

webdriver.close()
