"""

Selenium Flask Backend
Created by: jseow
version: 0.1

"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib.parse as urlparse
import requests
import time

from env import client_id, client_secret, redirect_uri, scope, state


# initializes flask application
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST', 'GET'])
def get_access_token():
    if request.method == 'POST':
        # get the email and password of user
        content = request.get_json()
        email = content['email']
        password = content['password']
        timeout = 10

        # chrome options for webdriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(chrome_options=chrome_options)

        driver_url = "https://api.ciscospark.com/v1/authorize?client_id={}&response_type=code&redirect_uri={}&scope={}&state={}".format(
            client_id, urlparse.quote(
                redirect_uri, safe=""), urlparse.quote(scope, safe=""), state
        )
        driver.get(driver_url)

        # start of webscrapping
        # every try/except is an action to the ciscospark website

        # enter
        try:
            inputElement = EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input.cui-input'))
            WebDriverWait(driver, timeout).until(inputElement)
            inputBox = driver.find_element_by_css_selector('input.cui-input')
            inputBox.clear()
            inputBox.send_keys(email)
            inputBox.send_keys(Keys.RETURN)
        except TimeoutException:
            print("Timed out waiting for page to load")
        try:
            usernameElement = EC.visibility_of_element_located(
                (By.NAME, 'pf.username'))
            WebDriverWait(driver, timeout).until(usernameElement)
            inputBox = driver.find_element_by_name('pf.username')
            inputBox.clear()
            inputBox.send_keys(email)
            inputBox.send_keys(Keys.RETURN)
        except TimeoutException:
            print("Timed out waiting for page to load")
        try:
            passwordElement = EC.visibility_of_element_located(
                (By.NAME, 'pf.pass'))
            WebDriverWait(driver, timeout).until(passwordElement)
            inputBox = driver.find_element_by_name('pf.pass')
            inputBox.clear()
            inputBox.send_keys(password)
            inputBox.send_keys(Keys.RETURN)
        except TimeoutException:
            print("Timed out waiting for page to load")
        #
        try:
            duoElement = EC.visibility_of_element_located(
                (By.ID, 'duo_iframe'))
            WebDriverWait(driver, timeout).until(duoElement)
            driver.switch_to.frame(driver.find_element_by_id('duo_iframe'))
            driver.find_element_by_css_selector('.auth-button').click()
        except TimeoutException:
            print("Timed out waiting for page to load")
        time.sleep(8)
        driver.switch_to.default_content()
        try:
            nextUrl = driver.current_url
            if "https://idbroker.webex.com/idb/oauth2" in nextUrl:
                driver.find_element_by_css_selector(
                    'button.cui-button--blue').click()
            googleElement = EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.content'))
            WebDriverWait(driver, timeout).until(googleElement)

        except TimeoutException:
            print("Timed out waiting for page to load")

        # get the final code from url after all the login and clicking
        # close the driver
        code_url = driver.current_url
        driver.close()
        parsed = urlparse.urlparse(code_url)
        code = urlparse.parse_qs(parsed.query)['code']

        # send request to get access token
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri
        }
        req = requests.post(
            "https://api.ciscospark.com/v1/access_token", data=data)

        # return the access token to the login page
        return jsonify(req.json())

    elif request.method == 'GET':
        return 'Hello World!'
