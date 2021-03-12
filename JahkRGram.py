
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from random import randint, randrange
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pandas as pd
import time
import random
import re

PER_HOUR = 24
SECONDS_PER_DAY = 86400
WAIT_TIME = 10   # DEFAULT: 10 Seconds to wait between each action
NUM_ACTIONS = 16  # Determined by number of sleep methods
CONTENT_PER_SCROLL = 15

# Calculates the pace of likes in a 24 hour period
MAX_LIKED = ((SECONDS_PER_DAY / WAIT_TIME) / NUM_ACTIONS) / PER_HOUR

# Calculates the number of page scrolls
NUM_PAGE_SCROLLS = int(MAX_LIKED / CONTENT_PER_SCROLL)


class JahkRBot:
    """JahkRBot Class with methods for in-browser actions."""

    def __init__(self, username, password):
        """Initialize Bot with class-wide variables."""
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def login(self):
        """Login to Instagram.
        xPath -> "//a[@href='accounts/login']"
        xPath -> "//input[@name='username']"
        xPath -> "//input[@name='password']"

        https://www.instagram.com/accounts/login/
        """
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

        username_elem = driver.find_element_by_xpath(
            "//input[@name='username']")
        username_elem.clear()
        for letter in self.username:
            username_elem.send_keys(letter)
            time.sleep(randrange(2))
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

        password_elem = driver.find_element_by_xpath(
            "//input[@name='password']")
        password_elem.clear()
        for letter in self.password:
            password_elem.send_keys(letter)
            time.sleep(randrange(2))
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

        password_elem.send_keys(Keys.RETURN)
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

    def getContent(self, hashtag):
        """Likes photo/video with tag given as argument."""
        driver = self.driver
        driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

        # Get Content
        content_hrefs = []
        for _ in range(NUM_PAGE_SCROLLS):
            try:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

                hrefs_in_view = driver.find_elements_by_tag_name('a')
                hrefs_in_view = [elem.get_attribute(
                    'href') for elem in hrefs_in_view
                    if '.com/p/' in elem.get_attribute('href')]

                [content_hrefs.append(href)
                    for href in hrefs_in_view if href not in content_hrefs]
                print(f'{hashtag} content: {str(len(content_hrefs))}')
            except Exception:
                continue
        return content_hrefs

    def likesIt(self, content_hrefs, hashtag, comment, OE_hashtags):
        ''' Determines if content was previously liked, and Likes content '''
        driver = self.driver
        totalLiked = 0
        unique_content = len(content_hrefs)
        liked_csv = pd.read_csv('logLiked_XadeIG.csv', encoding='utf-8-sig').to_dict()
        liked_csv = list(liked_csv['liked'].values())

        for content_href in content_hrefs:
            try:
                logLiked = open('logLiked_XadeIG.csv', 'a')
                driver.get(content_href)
                #driver.execute_script(
                #    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(randrange(WAIT_TIME))
                
                if content_href in liked_csv:
                    print(f'CONTENT ALREADY LIKED MOVING ON: {content_href}')
                else:
                    likeBtn = lambda: driver.find_element_by_class_name('_8-yf5')
                    self.commentOnIt(content=content_href, comment=comment, hashtags=OE_hashtags)
                    #postBtn = lambda: driver.find_element_by_class_name('sqdOP yWX7d y3zKF ')
                    #postBtn().click()
                    #likeBtn().click()
                    '''
                    if self.getComment() == '':
                        return
                    '''
                    #self.JahkRAIComment()
                    time.sleep(randrange(WAIT_TIME))

                    logLiked.write(f'{content_href},\n')
                    print(f'JahkRBot liked/commented {content_href}\n')
                    totalLiked += 1
                    for second in reversed(range(randint(int(WAIT_TIME), WAIT_TIME * 2))):
                        print(
                            f'#{hashtag} : unique content remaining: '
                            f'{str(unique_content)}'
                            f'| Sleeping {str(second)}')
                        time.sleep(randrange(WAIT_TIME))

            except (TimeoutError, NoSuchElementException) as e:
                print(f'Error occurred while liking content: {e}')
                time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

            unique_content -= 1

        print(f'JahkRBot liked {totalLiked} pieces of content.')

    def getComment(self):
        ''' Gets the content comment by uploader and response. Saves to dataset. '''
        time.sleep(randrange(WAIT_TIME))
        logCommented = open('a.csv', 'a')
        driver = self.driver
        try:
            commentsBlock = driver.find_element_by_class_name('XQXOT')
            commentsInBlock = commentsBlock.find_elements_by_class_name('gElp9')
            commentsBlock.send_keys(Keys.HOME)

            time.sleep(randint(int(WAIT_TIME),WAIT_TIME * 2))

            comments = [x.find_element_by_tag_name('span') for x in commentsInBlock]
            
            time.sleep(randrange(WAIT_TIME))
            userComment = re.sub(r'#.\w*', '', comments[0].text)
            userResponse = re.sub(r'#.\w*', '', comments[1].text)
            if userComment == '' and len(comments) >= 3:
                print(f'Reassigning userComment to {comments[-1].text}')
                userComment = re.sub(r'#.\w*', '', comments[-1].text)
            elif userComment == '' and len(comments) <= 2:
                print('Could not find userComment: SKIPPED')
                return ''
            elif len(comments) <= 1:
                return '' 
            # Writing responses for dataset
            logCommented.write(f'{userComment},\n')
            logCommented.write(f'{userResponse},\n')
            print(f'***** User: {userComment}\n***** Response: {userResponse}')
            logCommented.close()
            
        except (ElementNotInteractableException, IndexError, NoSuchElementException, StaleElementReferenceException):
            return ''
        return userComment

    def commentOnIt(self, content, comment, hashtags):
        ''' Writes comment in text area using lambda function. '''
        driver = self.driver

        
        hashtag_1 = random.choice(hashtags)
        hashtag_2 = random.choice(hashtags)
        if hashtag_1 == hashtag_2:
            hashtag_2 = random.choice(hashtags)
            
        currentResponse = f'{random.choice(comment)} {hashtag_1} {hashtag_2} 💖'
        #driver.get(f'https://www.instagram.com/p/{content}/')
        driver.get(content)
        time.sleep(randrange(WAIT_TIME))
        try:
            commentBtn = driver.find_elements_by_class_name('_8-yf5')[1]
            commentBtn = lambda: driver.find_element_by_css_selector("[aria-label=Comment]")
            commentBtn().click()
            time.sleep(randrange(WAIT_TIME))
        except NoSuchElementException as e:
            print(f'Error occurred while opening comment section: {e}')
        
        try:
            writeComment = driver.find_element_by_class_name('Ypffh')
            writeComment = lambda: driver.find_element_by_css_selector("[aria-label='Add a comment…']")
            writeComment().send_keys('')
            writeComment().clear()
            time.sleep(randint(int(WAIT_TIME), WAIT_TIME * 2))
            for letter in currentResponse:
                writeComment().send_keys(letter)
                time.sleep(randrange(2))
            writeComment().send_keys(Keys.RETURN)
            time.sleep(randint(int(WAIT_TIME), WAIT_TIME * 2))
            writeComment().send_keys(Keys.RETURN)
            time.sleep(randint(int(WAIT_TIME), WAIT_TIME * 2))
            writeComment().send_keys(Keys.RETURN)
            
        except NoSuchElementException and StaleElementReferenceException as e:
            print(f'Error occurred while writing comment: {e}')
            return False
        
        return writeComment
    
    # TODO: Add AI functionality once dataset is built and trained
    def JahkRAIComment(self):
        bot = ChatBot('JahkRAI')
        trainer = ListTrainer(bot)
        contentComment = self.getComment()

        response = bot.get_response(contentComment)
        print(f'Content Comment: {contentComment}')
        print(f'JahkRAI Response: {response}')
        return self.commentOnIt(response)
    
    def closeBrowser(self):
        """Closes browser."""
        self.driver.close()

# TODO: Add decorator to track duration between each action
