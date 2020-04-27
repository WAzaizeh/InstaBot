import Constants
from selenium import webdriver as Webdriver
from selenium.webdriver import ChromeOptions
import AccountAgent
from csvHandler import csvHandler
from multiprocessing import Process
import logging


# use seperate log files for unfollow and follow
def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)


def _get_webdriver(developer_mode=0):
    chromedriver_path = Constants.CHROME_DRIVER_PATH
    opts = ChromeOptions()
    if developer_mode > 1:
        opts.add_experimental_option("detach", True)
    if developer_mode > 0 and developer_mode < 3:
        opt.add_argument('headless')
    webdriver = Webdriver.Chrome(executable_path=chromedriver_path, chrome_options=opts)
    return webdriver


def _close_webdriver(webdriver):
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
    # setup logger for unfollow
    unfollow_logger = 'log1'
    setup_logger(unfollow_logger, os.getcwd()+'/temp/unfollow.log')
    log1 = logging.getLogger(unfollow_logger)
    log1.info('Checking for users to unfollow..')

    # get the lists of users to unfollow
    db = csvHandler()
    db.__init__()
    users = db.check_unfollow_list()

    #if there's anyone in the list, start unfollowing operation
    if len(users) > 0:
        log1.info('Unfollowing [{}] users...'.format(len(users)))
        webdriver = _get_webdriver(developer_mode=developer_mode)
        AccountAgent.login(webdriver, logger=unfollow_logger)
        AccountAgent.unfollow_people(webdriver, users, logger_name=unfollow_logger)
        _close_webdriver(webdriver)
    else:
        log1.info("No users to unfollow at the moment...")


def _follow_new_users(developer_mode):
    # setup logger for unfollow
    follow_logger = 'log2'
    setup_logger(unfollow_logger, os.getcwd()+'/temp/follow.log')
    log2 = logging.getLogger(unfollow_logger)
    log2.info('Checking for users to unfollow..')

    # follow new users
    log2.info('Starting to follow & like new users..')
    webdriver = _get_webdriver(developer_mode=developer_mode)
    AccountAgent.login(webdriver, logger_name=follow_logger)
    AccountAgent.follow_people(webdriver, logger_name=follow_logger)
    _close_webdriver(webdriver)
