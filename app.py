#!usr/bin/env python

import os
import sys
import time

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Selenium Exceptions
from selenium.common.exceptions import TimeoutException

class Bot:
  def __init__(self, username: str, password: str) -> None:
    self.username = username
    self.password = password

    # Create Two Directory First
    try:
      dirs = ['Jobs', 'data']
      for dir in dirs: os.mkdir(os.path.join(os.getcwd(), dir))
    except: pass

    # Options
    options = Options()
    option_path = os.path.join(os.getcwd(), 'data')
    options.arguments.append(f'user-data-dir={option_path}')

    # Driver PATH
    if sys.platform == 'linux':
      path = os.path.join(os.getcwd(), 'chromedriver')
    elif sys.platform.startswith('win'):
      path = os.path.join(os.getcwd(), 'chromedriver.exe')
    self.driver = webdriver.Chrome(executable_path=path, options=options)

    # Get Some Cookies First
    # sites = [
    #   'https://google.com/',
    #   'https://youtube.com/',
    #   'https://yahoo.com/',
    # ]
    # for site in sites:
    #   self.driver.get(site)
    #   time.sleep(6)

  def login(self):
    self.driver.get('https://www.upwork.com/ab/account-security/login')

    # Username Field
    username_field = self.driver.find_element(By.ID, 'login_username')
    username_btn = self.driver.find_element(By.ID, 'login_password_continue')

    username_field.send_keys(self.username)
    time.sleep(1)
    username_btn.click()
    time.sleep(4)

    # Password Field
    password_field = self.driver.find_element(By.ID, 'login_password')
    password_btn = self.driver.find_element(By.ID, 'login_control_continue')
    checkbox = self.driver.find_element(By.CLASS_NAME, 'up-checkbox-replacement-helper')

    password_field.send_keys(self.password)
    time.sleep(1)
    checkbox.click()
    password_btn.click()
    time.sleep(4)

  def browse(self):
    self.driver.get('https://www.upwork.com/ab/proposals/archived')
    time.sleep(4)
    links_all = list(self.driver.find_elements(By.XPATH, '//div[@class="pb-5"]/a'))

    # Collect Every Data
    links = []
    while True:
      for link in links_all:
        links.append(link.get_attribute('href'))
        # time.sleep(2)
      try:
        paginate = self.driver.find_element(By.XPATH, '//*[@id="archived"]/div/div[1]/footer/div/nav/ul/li[6]/button')
        paginate.click()
      except:
        break
    
    # Browse Every Link
    for link in links:
      self.collect(link)

  def collect(self, url):
    self.driver.get(url)
    time.sleep(2)
    job_title = self.driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div/div[1]/div/div[1]/up-proposal-job-details/section/div[1]/div[1]/h3').text
    self.driver.execute_script("document.getElementsByClassName('p-0-bottom')[0].scrollIntoView();")
    time.sleep(2)

    try:
      wait = WebDriverWait(self.driver, 10)
      element = wait.until(EC.element_to_be_clickable((By.XPATH, '//p/span/a')))
      self.driver.find_element(By.XPATH, '//p/span/a').click()
      cover_letter = self.driver.find_element(By.XPATH, '//p/span/span[@class="ng-scope"]').text
    except TimeoutException: pass

    cover_letter = self.driver.find_element(By.XPATH, '//p[@class="break text-pre-line m-md-bottom ng-scope ng-isolate-scope"]').text

    print(job_title)
    print(cover_letter)

    with open(os.path.join(os.getcwd(), 'Jobs', job_title + '.txt'), 'w') as f:
      f.write(job_title + '\n\n' + cover_letter.strip(' less'))
    return

def main():
  # User Credntials
  username = 'rafsanbillah@gmail.com'
  password = 'RYT.Yeasin@@010'

  # Bot
  b = Bot(username=username, password=password)
  b.login()
  b.browse()

if __name__ == '__main__':
  main()