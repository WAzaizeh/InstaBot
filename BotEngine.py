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

def close_driver(webdriver):
    webdriver.close()

def update(follow=True, developer_mode=False):
    p1 = Process(target = _check_follow_list, args = ((developer_mode,)))
    p1.start()
    if follow:
        p2 = Process(target = _follow_new_users, args = ((developer_mode,)))
        p2.start()

    p1.join()
    if follow:
        p2.join()


def _check_follow_list(developer_mode):
    print('Checking for users to unfollow..')
    # get the lists of users to unfollow
    db = csvHandler()
    db.__init__()
    users = db.check_unfollow_list()
    #if there's anyone in the list, start unfollowing operation
    if len(users) > 0:
        print('Unfollowing [{}] users...'.format(len(users)))
        webdriver = get_webdriver(developer_mode=developer_mode)
        AccountAgent.login(webdriver)
        AccountAgent.unfollow_people(webdriver, users)
        close_driver(webdriver)
    else:
        print("No users to unfollow at the moment...")

def _follow_new_users(developer_mode):
    webdriver = get_webdriver(developer_mode=developer_mode)
    AccountAgent.login(webdriver)
    AccountAgent.follow_people(webdriver)
    close_driver(webdriver)
