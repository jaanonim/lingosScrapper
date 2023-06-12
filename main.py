import random
import string

from selenium import webdriver
import time
import json
from translation import translations
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

HEADLESS = False
MISTAKES_CHASE = 0.05

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
opt.add_argument("--mute-audio")
if HEADLESS:
    opt.add_argument('--headless')
opt.add_experimental_option(
    "prefs",
    {
        "profile.default_content_setting_values.media_stream_mic": 2,
        "profile.default_content_setting_values.media_stream_camera": 2,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.notifications": 2,
    },
)

# start browser
driver = webdriver.Chrome(options=opt)


# get login creds from creds.json
def get_creds():
    data = None
    with open("creds.json") as json_file:
        data = json.load(json_file)
        return data["email"], data["password"]


def start_browser():
    driver.get("https://lingos.pl/home/login")

    # wait for page
    WebDriverWait(driver, 10000).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )


def login():
    # get creds for login
    email, password = get_creds()
    email_field = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/input')
    email_field.click()
    email_field.send_keys(email)

    password_field = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[2]/input')
    password_field.click()
    password_field.send_keys(password + Keys.ENTER)

    time.sleep(2)


def start_lesson():
    try:
        start_lesson_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[1]/div/div[2]/a')
        start_lesson_btn.click()
        time.sleep(0.5)
    except NoSuchElementException:
        return False
    except ElementClickInterceptedException:
        return False
    return True


def loop():
    while True:
        try:
            next_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/button')
            next_btn.click()
            time.sleep(0.5)
        except NoSuchElementException:
            pass

        try:
            text = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/h3')

            input_field = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/form/div/input')
            input_field.click()
            input_field.send_keys(translate(text.text) + Keys.ENTER)
            time.sleep(0.5)
        except NoSuchElementException:
            pass

        try:
            ok_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/a')
            ok_btn.click()
            time.sleep(0.5)
        except NoSuchElementException:
            pass

        if driver.current_url == "https://lingos.pl/students/group/finished":
            try:
                close_btn = driver.find_element(By.XPATH, '//*[@id="sessionFinishedModal"]/div/div/div[2]/button')
                close_btn.click()
                time.sleep(0.1)
            except NoSuchElementException:
                pass
            break


def translate(text):
    alphabet = list(string.ascii_lowercase)
    res = translations[text]
    if random.random() < MISTAKES_CHASE:
        if random.random() < 0.7:
            l_res = list(res)
            l_res[random.randrange(0, len(res) - 1)] = random.choice(alphabet)
            res = "".join(l_res)
        else:
            res = random.choice(list(translations.values()))
    return res


def main():
    print("Starting...")
    start_browser()
    print("Browser: DONE")
    login()
    print("Login: DONE")
    while True:
        print("Starting lesson...")
        if not start_lesson():
            break
        loop()
        print("Lesson: DONE")
        if not HEADLESS:
            input("Press enter to start next lesson...")
    print("No more lessons")
    if not HEADLESS:
        input("Press enter to exit...")


if __name__ == '__main__':
    main()
