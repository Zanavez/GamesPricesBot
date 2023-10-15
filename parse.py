from selenium import webdriver
import time


def steam_parse():
    driver = webdriver.Edge()
    driver.get("https://store.steampowered.com/")
    search_string = driver.find_element('id', 'store_nav_search_term')
    search_string.send_keys("Baldur's Gate 3")
    search_string.submit()
    time.sleep(3)
    driver.quit()


steam_parse()