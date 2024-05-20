from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from selenium.webdriver.common.by import By
import time

cap:Dict[str, Any]={
  "platformName": "Android",
  "deviceName": "Pixel3",
  "automationName": "UiAutomator2",
  "appPackage": "org.telegram.messenger.web",
  "appActivity": "org.telegram.messenger.DefaultIcon",
  "fullReset": False,
  "noReset": True
}
url = 'http://host.docker.internal:4723/wd/hub'
#url = 'http://localhost:4723/wd/hub'

driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(cap))

# stored xpaths for button / text fields detection and use
START_BOT_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[3]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.TextView'
RESTART_BOT_XPATH =  '//android.view.View[@content-desc="RESTART"]'
SEARCH_BAR_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[4]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.EditText'
PNG_TEST_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.View'
ATTACH_MEDIA_XPATH = '//android.widget.ImageView[@content-desc="Attach media"]'
MORE_OPTIONS_BUTTON_XPATH = '//android.widget.ImageButton[@content-desc="More options"]/android.widget.ImageView'
SEND_AS_FILE_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.widget.TextView'
JPG_TEST_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.View'
SEND_PHOTO_XPATH = '//android.widget.ImageView[@content-desc="Send"]'
BACK_TO_GALLERY_XPATH = '//android.widget.ImageView[@content-desc="Go back"]'
PHOTO_SELECT_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.CheckBox'
MESSAGE_TEXTBOX_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[3]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.EditText'
SEND_BUTTON_XPATH = '//android.view.View[@content-desc="Send"]'
SEARCH_BUTTON_XPATH = '//android.widget.ImageButton[@content-desc="Search"]/android.widget.ImageView'
BOT_ON_SEARCH_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[4]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]'

def assure_button_click(button_xpath: str):
  """
  assure_button_click assures finding wanted elements, because
  xpath can cause problems finding the wanted
  elements from time to time.

  :button_xpath: the wanted xpath, which the function will assure its been found
  :return: the wanted element that was found
  """

  while True:
    try:
      found_element = driver.find_element(By.XPATH, button_xpath)
      return found_element
    except:
      continue

def send_photo(photo_xpath: str):
  """
  send_photo function is being used when needed to
  send a picture to the bot.

  :photo_xpath: the wanted photo's xpath in the gallery
  """

  global driver

  # clicking on attach media button
  driver.find_element(By.XPATH, ATTACH_MEDIA_XPATH).click()
  time.sleep(0.5)

  # clicking on the photo
  driver.find_element(By.XPATH, photo_xpath).click()
  time.sleep(0.5)

  # selecting the photo
  driver.find_element(By.XPATH, PHOTO_SELECT_XPATH).click()
  time.sleep(0.5)

  # going back to the photo selection
  driver.find_element(By.XPATH, BACK_TO_GALLERY_XPATH).click()
  time.sleep(0.5)

  # sending photo as file, so it wont be converted to JPG automatically by telegram
  driver.find_element(By.XPATH, MORE_OPTIONS_BUTTON_XPATH).click()
  time.sleep(0.5)
  driver.find_element(By.XPATH, SEND_AS_FILE_XPATH).click()
  time.sleep(0.5)

def start_bot_chat():
  """
  start_bot_chat function is responsible
  for finding and starting the chat with
  the bot on telegram.
  """

  BOT_NAME = "IdansHWBot"

  driver.find_element(By.XPATH, SEARCH_BUTTON_XPATH).click()
  time.sleep(0.5)

  # Opening search bar and searching the bots name
  search_bar_element = assure_button_click(SEARCH_BAR_XPATH)
  search_bar_element.click()
  search_bar_element.send_keys(BOT_NAME)
  time.sleep(0.5)

  # Clicking on the bot after searching for it
  driver.find_element(By.XPATH,BOT_ON_SEARCH_XPATH).click()
  time.sleep(0.5)

  # Clicking on start bot after finding it
  # first try to /start
  try:
    driver.find_element(By.XPATH, START_BOT_XPATH).click()
  except:
    # means that the bot was already started, just needs to be restarted
    try:
      driver.find_element(By.XPATH, RESTART_BOT_XPATH).click()
    except:
      # in case the bot was already started/restarted, no action needs to be made
      pass

  time.sleep(0.5)

def send_text_messages():
  """
  send_text_messages function is the last test
  function, which is sending texts to the bot.
  """

  FIRST_TEST_MESSAGE = "This is the 1st test!"
  SECOND_TEST_MESSAGE = "Test number 2"

  # locating the textbox element and sending the messages
  textbox_element = assure_button_click(MESSAGE_TEXTBOX_XPATH)

  textbox_element.send_keys(FIRST_TEST_MESSAGE)
  assure_button_click(SEND_BUTTON_XPATH).click()
  time.sleep(0.5)

  textbox_element.send_keys(SECOND_TEST_MESSAGE)
  assure_button_click(SEND_BUTTON_XPATH).click()
  time.sleep(0.5)

def main():
  try:
    # Entering the chat with the bot
    start_bot_chat()
    time.sleep(0.5)

    # Sending the photos - first the PNG, then JPG
    send_photo(PNG_TEST_XPATH)
    time.sleep(0.5)
    send_photo(JPG_TEST_XPATH)

    # Sending text messages
    send_text_messages()

    time.sleep(6)
    driver.quit()
  except:
    print("Something went wrong.")
    driver.quit()

if __name__ == "__main__":
    main()
