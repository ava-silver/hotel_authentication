#!/usr/bin/env python3

from sys import argv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException, WebDriverException)
from urllib.parse import urlparse
BUTTON_XPATH: str = '/html/body/div[2]/div/div[1]/div[2]/div[1]/section[4]/div/div/div/div/form/div[2]/button'


def log_min(*args):
    if args and 'connect button' in args[0]:
        print('.', end='')
    else:
        print()
        print(*args)


def ignore(*args):
    pass


def main(args):
    if len(args) > 2:
        print('invalid usage, try either "-h", "-q", "-v", or no arguments')
        return
    if '-v' in args:
        log = print
    elif '-q' in args:
        log = ignore
    else:
        log = log_min

    options = webdriver.FirefoxOptions()
    options.headless = True
    responded = False
    browser = webdriver.Firefox(options=options)
    while not responded:
        try:
            browser.get('http://detectportal.firefox.com/canonical.html')
            responded = True
        except WebDriverException as e:
            log(e.msg)
            if "Timeout" not in str(e.msg):
                return
            browser.close()
            browser = webdriver.Firefox(options=options)

    browser.set_page_load_timeout(15)
    connect_button = None
    while connect_button is None:
        browser.implicitly_wait(1)
        try:
            if (hostname := urlparse(browser.current_url).hostname) == 'support.mozilla.org':
                log('Already Connected')
                return
            log(
                f'trying to find connect button on {hostname}')
            connect_button = browser.find_element(By.XPATH, BUTTON_XPATH)
        except NoSuchElementException:
            pass

    log('found connect button!')
    connect_button.click()
    browser.implicitly_wait(3)
    browser.close()
    log('Connected')


if __name__ == '__main__':
    main(argv)
