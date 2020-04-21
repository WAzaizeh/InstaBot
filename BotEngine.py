import Constants
from selenium import webdriver as Webdriver
from selenium.webdriver import ChromeOptions
import AccountAgent
from csvHandler import csvHandler
import datetime
from multiprocessing import Process

def init():
    # initialize Constants to get the values from "settings.json"
    Constants.init()

def get_webdriver(developer_mode=False):
    chromedriver_path = Constants.CHROME_DRIVER_PATH
    opts = ChromeOptions()
    if developer_mode:
        # change selenium settings to stay open when session is terminated
        opts.add_experimental_option("detach", True)
    webdriver = Webdriver.Chrome(executable_path=chromedriver_path, chrome_options=opts)
    return webdriver

def update(follow=True, developer_mode=False):
    p1 = Process(target = _check_follow_list)
    p1.start()
    if follow:
        p2 = Process(target = _follow_new_users)
        p2.start()

    p1.join()
    if follow:
        p2.join()


def _check_follow_list():
    print('Checking for users to unfollow..')
    # get the lists of users to unfollow
    db = csvHandler()
    users = db.check_unfollow_list()
    #if there's anyone in the list, start unfollowing operation
    if len(users) > 0:
        print('Unfollowing [{}] users...'.format(len(users)))
        webdriver = get_webdriver()
        AccountAgent.login(webdriver)
        AccountAgent.unfollow_people(webdriver, users)

def _follow_new_users():
    webdriver = get_webdriver()
    AccountAgent.login(webdriver)
    AccountAgent.follow_people(webdriver)
