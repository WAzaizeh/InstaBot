from time import sleep
import datetime as dt
import Constants, TimeHelper
import traceback
import random
from csvHandler import csvHandler
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import sys


def login(webdriver):
    # Open the instagram login page
    webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    # Sleep for 3 seconds to prevent issues with the server
    sleep(3)
    # Find username and password fields and set their input using our constants
    print('Logging in....')
    username = webdriver.find_element_by_name('username')
    username.send_keys(Constants.INST_USER)
    password = webdriver.find_element_by_name('password')
    password.send_keys(Constants.INST_PASS)
    # Sleep for 2 seconds to prevent issues with server
    sleep(2)
    password.send_keys(Keys.RETURN)
    # Check if login succeeded
    try:
        user_image_xpath = "//a/img[contains(@alt,'profile picture')]"
        WebDriverWait(webdriver, 10).until(EC.visibility_of_element_located((By.XPATH, user_image_xpath)))
        print('Login complete')
    except NoSuchElementException:
        print('NoSuchElementException \nLogin failed...')
        webdriver.close()
    except TimeoutException as ex:
        print('TimeoutException \nLogin failed...')
        webdriver.close()
    #In case you get a popup after logging in, press not now
    sleep(3)
    try:
        notnow_css = 'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm'
        WebDriverWait(webdriver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, notnow_css)))
        notnow = webdriver.find_element_by_css_selector(notnow_css)
        notnow.click()
    except NoSuchElementException:
        return

def unfollow_people(webdriver, people):
    # if only one user, append in a list
    if not isinstance(people, (list,)):
        p = people
        people = []
        people.append(p)

    # direct prints to a log file

    removed = 0
    for i,user in enumerate(people):
        webdriver.get('https://www.instagram.com/' + user + '/')
        # sleep for 3 seconds to prevent issues with the server
        sleep(3)
        unfollow_check_xpath = '//span[contains(@aria-label, "Following")]'
        unfollow_confirm_xpath = '//button[contains(text(), "Unfollow")]'
        # unfollow_confirm_css = 'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.-Cab_'

        # follow only if the Follow button exists
        tries = 0
        while tries < 2: # Try refreshing page if NoSuchElementException is raised
            try:
                WebDriverWait(webdriver, 10).until(EC.visibility_of_element_located((By.XPATH, unfollow_check_xpath)))
            except NoSuchElementException:
                webdriver.refresh()
            except Exception as e:
                print('This user isn\'t followed')
            else:
                sleep(random.randint(1, 7))
                webdriver.find_element_by_xpath(unfollow_check_xpath+'/../..').click()
                sleep(2)
                WebDriverWait(webdriver, 10).until(EC.visibility_of_element_located((By.XPATH, unfollow_confirm_xpath)))
                webdriver.find_element_by_xpath(unfollow_confirm_xpath).click()
                removed += 1
                csvHandler.delete_user(user)
                sleep(random.randint(1, 4))
                print('[{0}/{1}] {2} unfollowed'.format(removed, len(people), username))
                break
            tries += 1

def follow_people(webdriver):
    # get and store all the followed user
    db = csvHandler()
    db.__init__()
    prev_user_list = db.get_followed_users()
    new_followed = []

    # counters
    followed = 0
    likes = 0

    # run for the specified duration
    run_timer_start = dt.datetime.now()
    while TimeHelper.minutes_since(run_timer_start) < Constants.RUN_DURATION:
        # iterate theough all the hashtags from the constants
        for hashtag in Constants.HASHTAGS:
            # visit the hashtag
            webdriver.get('https://www.instagram.com/explore/tags/' + hashtag+ '/')
            sleep(5) # to prevent issues with the server

            # start from the 1st most recent post
            start = dt.datetime.now()
            print('Starting to follow & like new users under #{}....'.format(hashtag))
            most_recent_xpath = '//article/div[2]/div/div[1]/div[1]/a/div[1]'
            WebDriverWait(webdriver, 10).until(EC.visibility_of_element_located((By.XPATH, most_recent_xpath)))
            most_recent = webdriver.find_element_by_xpath(most_recent_xpath)
            most_recent.click()
            sleep(random.randint(1,3))

            # iterate over the most recent hashtags for the next 10 minutes
            while TimeHelper.minutes_since(start) < Constants.CHECK_FOLLOWERS_EVERY:
                # get the poster's username
                tries = 0
                while tries < 2:
                    try:
                        username_xpath = '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a'
                        username = webdriver.find_element_by_xpath(username_xpath).text
                        print("Detected: {0}".format(username))
                    except NoSuchElementException:
                        webdriver.refresh()
                        tries += 1
                    else:
                        # get number of likes and compare it to the maximum number of likes to ignore post
                        likes_over_limit = False
                        like_button_xpath = '//*/span[@class="fr66n"]/button[@type="button"]'
                        likes_num_xpath = '//*/div[@class="Nm9Fw"]/button[@type="button"]/span'
                        try: # get number of likes if there is any
                            likes_num = webdriver.find_element_by_xpath(likes_num_xpath).text
                            likes_num = int(likes_num.replace(',', '')) # strip the comma if there's any
                        except:
                            likes_num = 0 # if the post has no likes
                        if likes_num > Constants.LIKES_LIMIT:
                            print("likes over {0}".format(Constants.LIKES_LIMIT))
                            likes_over_limit = True

                        # if username isn't stored in the database and the likes are in the acceptable range
                        if username not in prev_user_list and not likes_over_limit:
                            # confirm that the Follow button is visible before clicking
                            follow_button_xapth = "//div[@class='bY2yH']/button[contains(text(), 'Follow')]"
                            try:
                                follow_button = webdriver.find_element_by_xpath(follow_button_xapth)
                                follow_button.click()
                                csvHandler.add_user(username)
                                followed += 1
                                print("Followed: {0}, #{1}".format(username, followed))
                                new_followed.append(username)
                            except NoSuchElementException:
                                print('Couldn\'t find Follow button for {}'.format(username))
                                continue

                        # Liking the picture
                        button_like = webdriver.find_element_by_xpath(like_button_xpath)
                        button_like.click()
                        likes += 1
                        print("Liked {0}'s post, #{1}".format(username, likes))
                        sleep(random.randint(5, 18))


                # Next picture
                webdriver.find_element_by_link_text('Next').click()
                sleep(random.randint(5, 10))


            #add new list to old list
            for n in range(0, len(new_followed)):
                prev_user_list.append(new_followed[n])
            print('For #{}:'.format(hashtag))
            print('Liked {} photos.'.format(likes))
            print('Followed {} new people.'.format(followed))
