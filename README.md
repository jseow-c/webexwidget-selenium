# Selenium Solution for Webex Widget

## Introduction

The implementation serves to assist anyone who needs to make a frontend seamless for webex-widgets.

This solution comprises of 2 parts

- a regular HTML/JS/CSS Frontend
- Flask/Selenium Backend (utilizes chrome webdriver - you may choose to use any others that provides headless solution)

## Implementation

To start, you need to create a virtual environment for the Python Backend. To do that, you can execute the following codes
`python -m venv webex-env`
`./webex-env/Scripts/activate`
Then, you can install the Python packages required.
`pip install -r requirements.txt`
Finally, add in an `env.py` file as per in the `env.py.example`. You are required to have your own Integration application in order for this to work. Please refer to https://webex.developer.com for more information under Integration.
