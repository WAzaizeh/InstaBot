import Constants
from selenium import webdriver as Webdriver
from selenium.webdriver import ChromeOptions
import AccountAgent
from csvHandler import csvHandler
from multiprocessing import Process

def get_webdriver(developer_mode=0):
    chromedriver_path = Constants.CHROME_DRIVER_PATH
    opts = ChromeOptions()
    if developer_mode > 1:
        opts.add_experimental_option("detach", True)
    if developer_mode > 0 and developer_mode < 3:
        opt.add_argument('headless')
    webdriver = Webdriver.Chrome(executable_path=chromedriver_path, chrome_options=opts)
    return webdriver

def close_driver(webdriver):
    webdriver.close()

def update(run_mode=0, developer_mode=0):
    if run_mode > 0:
        p1 = Process(target = _follow_new_users, args = ((developer_mode,)))
        p1.start()
    if not run_mode == 1:
        p2 = Process(target = _check_follow_list, args = ((developer_mode,)))
        p2.start()

    if run_mode > 0:
        p1.join()
    if not run_mode == 1:
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
    print('Starting to follow & like new users..')
    webdriver = get_webdriver(developer_mode=developer_mode)
    AccountAgent.login(webdriver)
    AccountAgent.follow_people(webdriver)
    close_driver(webdriver)
