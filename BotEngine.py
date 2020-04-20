import AccountAgent, csvHandler
import Constants
import datetime


def init(webdriver):
    AccountAgent.login(webdriver)


def update(webdriver, follow=True):
    # Get start of time to calculate elapsed time later
    start = datetime.datetime.now()
    # Before the loop, check if any users should be unfollowed
    _check_follow_list(webdriver)
    while follow:
        # Start following operation
        AccountAgent.follow_people(webdriver)
        # Get the time at the end
        end = datetime.datetime.now()
        # How much time has passed?
        elapsed = end - start
        # If greater than our constant to check on followers, check on followers
        if elapsed.total_seconds() >= Constants.CHECK_FOLLOWERS_EVERY:
            # #reset the start variable to now
            # start = datetime.datetime.now()
            # #check on followers
            # _check_follow_list(webdriver)
            # stop following after certain period
            follow = False


def _check_follow_list(webdriver):
    print("Checking for users to unfollow..")
    # get the lists of users to unfollow
    db = csvHandler()
    users = db.check_unfollow_list()
    #if there's anyone in the list, start unfollowing operation
    if len(users) > 0:
        AccountAgent.unfollow_people(webdriver, users)
