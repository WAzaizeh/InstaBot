from time import sleep
import datetime
import UsersHandler, Constants
import traceback
import random
from csvHandler import csvHandler
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

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
    password.send_keys(Keys.RETURN)
    print('Login complete')
    sleep(3)
    #In case you get a popup after logging in, press not now.
    #If not, then just return
    try:
        notnow = webdriver.find_element_by_css_selector(
            'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
        notnow.click()
    except:
        return

def unfollow_people(webdriver, people):
    #if only one user, append in a list
    if not isinstance(people, (list,)):
        p = people
        people = []
        people.append(p)

    removed = 0
    for i,user in enumerate(people):
        try:
            webdriver.get('https://www.instagram.com/' + user + '/')
            sleep(5)
            unfollow_xpath = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button'
            unfollow_confirm_css = 'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.-Cab_'

            # to optimize page opening need an xpath that isn't dependent on follow status
            if webdriver.find_element_by_xpath(unfollow_xpath).text == "Following":
                sleep(random.randint(1, 7))
                webdriver.find_element_by_xpath(unfollow_xpath).click()
                sleep(2)
                if webdriver.find_element_by_css_selector(unfollow_confirm_css).text == "Unfollow":
                    webdriver.find_element_by_css_selector(unfollow_confirm_css).click()
                    removed += 1
                else:
                    print("Couldn't Unfollow {}".format(user))
                    UsersHandler.delete_user(user)
                sleep(4)
            print('[{0}/{1}] Users removed'.format(removed, len(people)))

        except Exception:
            traceback.print_exc()
            continue


def follow_people(webdriver):
    # get and store all the followed user
    db = csvHandler()
    prev_user_list = db.get_followed_users()
    new_followed = []

    #counters
    followed = 0
    likes = 0

    # iterate theough all the hashtags from the constants
    for hashtag in Constants.HASHTAGS:
        # visit the hashtag
        webdriver.get('https://www.instagram.com/explore/tags/' + hashtag+ '/')
        sleep(5) # replace with DriverWait

        # start from the 1st most recent post
        print('Starting to follow and like under #{0}....'.format(hashtag))
        most_recent_xpath = '//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]'
        WebDriverWait(webdriver, 10).until(EC.visibility_of_element_located((By.XAPTH, most_recent_xpath)))
        most_recent = webdriver.find_element_by_xpath(most_recent_xpath)
        most_recent.click()
        sleep(random.randint(1,3))

        try:
            # iterate over the most recent hashtags for the next 10 minutes
            timer_start = datetime.datetime.now()
            while ((datetime.datetime.now() - timer_start).total_seconds() / 60.0) < Constants.CHECK_FOLLOWERS_EVERY:
                # get the poster's username
                username_xpath = '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a'
                username = webdriver.find_element_by_xpath(username_xpath).text
                print("Detected: {0}".format(username))

                # get number of likes and compare it to the maximum number of likes to ignore post
                likes_over_limit = False
                like_button_xpath = '//*/span[@class="fr66n"]/button[@type="button"]'
                likes_num_xpath = '//*/div[@class="Nm9Fw"]/button[@type="button"]/span'
                sleep(0.2)
                try:
                    likes_num = webdriver.find_element_by_xpath(likes_num_xpath).text
                    likes_num = int(likes_num.replace(',', '')) # strip the comma if there's any
                except NoSuchElementException:
                    likes_num = 0 # if the post has no likes
                if likes_num > Constants.LIKES_LIMIT:
                    print("likes over {0}".format(Constants.LIKES_LIMIT))
                    likes_over_limit = True

                # if username isn't stored in the database and the likes are in the acceptable range
                if username not in prev_user_list and not likes_over_limit:
                    #Don't press the button if the text doesn't say follow
                    if webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                        #Use UsersHandler to add the new user to the database
                        UsersHandler.add_user(username)
                        #Click follow
                        webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                        followed += 1
                        print("Followed: {0}, #{1}".format(username, followed))
                        new_followed.append(username)


                        # Liking the picture
                        button_like = webdriver.find_element_by_xpath(like_button_xpath)
                        button_like.click()
                        likes += 1
                        print("Liked {0}'s post, #{1}".format(username, likes))
                        sleep(random.randint(5, 18))


                # Next picture
                webdriver.find_element_by_link_text('Next').click()
                sleep(random.randint(10, 30))

        except:
            traceback.print_exc()
            continue

        #add new list to old list
        for n in range(0, len(new_followed)):
            prev_user_list.append(new_followed[n])
        print('For #{}:'.format(hashtag))
        print('Liked {} photos.'.format(likes))
        print('Followed {} new people.'.format(followed))
