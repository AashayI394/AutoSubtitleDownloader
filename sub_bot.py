import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# IMDb IDs for Marvel movies
marvel_movie_ids = [
    "tt0371746",  # Iron Man
    "tt0800080",  # The Incredible Hulk
    "tt1228705",  # Iron Man 2
    "tt0800369",  # Thor
    "tt0458339",  # Captain America: The First Avenger
    "tt0848228",  # The Avengers
    # Add more Marvel movie IMDb IDs as needed
]

# Set up WebDriver
# driver_path = "path_to_your_chromedriver"  # Replace with your WebDriver path
# driver = webdriver.Chrome(driver_path)

driver = webdriver.Chrome()

# Set up download directory
current_dir = os.getcwd()
subtitle_dir = os.path.join(current_dir, "subtitles")
os.makedirs(subtitle_dir, exist_ok=True)



# Function to scroll to the download link
def scroll_to_element(selector):
    element = None
    while not element:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)  # Wait a moment to allow for scrolling
            element.click()
            print(f"Clicked on element with selector: {selector}")
            return True
        except Exception as e:
            print(f"Element not found or not clickable yet: {e}")
            time.sleep(1)  # Wait before trying again
    return False



# Function to download subtitle
def download_subtitle(imdb_id):
    try:
        # Open OpenSubtitles website
        driver.get("https://www.opensubtitles.com/en/")

        # Find the search box and enter IMDb ID
        search_box = driver.find_element(By.ID, "form-search-input")
        search_box.clear()
        search_box.send_keys(imdb_id)
        
        search_button_ID = "button-search-submit"
        search_button = driver.find_element(By.ID, search_button_ID)
        search_button.click()
        
        #search_box.send_keys(Keys.RETURN)

        time.sleep(3)  # Wait for search results to load
        
        # Check and click cookie consent if present
        try:
            cookie_button = driver.find_elements(By.CSS_SELECTOR, "a.cc-btn.cc-dismiss")
            if cookie_button:  # Check if the list is not empty
                cookie_button[0].click()
                print("Cookie clicked if any.")
            else:
                print("No cookie consent button found.")
        except Exception as e:
            print(f"An error occurred while handling cookie consent: {e}")

        time.sleep(1)  # Wait for a second after clicking the cookie button

        # Click on the first subtitle result link
        try:
            new_class = "a.btn.btn-default.btn-block"
            if scroll_to_element(new_class):
                download_icon = driver.find_element(By.CSS_SELECTOR, new_class)
                download_icon.click()
                print("First download icon clicked successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(3)
        
        
        #clicking second download 
        try:
            new_class="a.btn.btn-default.download-trigger"
            if scroll_to_element(new_class):
                download_icon = driver.find_element(By.CSS_SELECTOR, new_class)
                download_icon.click()
                print("Second download icon clicked successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(3)



        new_class = "a.btn.btn-default.btn-block.btn-warning.no-opt-link"
        download_icon = driver.find_element(By.CSS_SELECTOR, new_class)
        download_icon.click()
        print("Waiting for timer to end (20 sec...)")
        time.sleep(22)  # Wait for the download to prepare
        
        new_class = "a.btn.btn-block.btn-warning"
        download_icon = driver.find_element(By.CSS_SELECTOR, new_class)
        download_icon.click()
        print(f"Downloading subtitle for {imdb_id}")
        time.sleep(2)  # Wait for the download to prepare

        print(f"Downloaded subtitle for IMDb ID: {imdb_id}")

    except Exception as e:
        print(f"Error downloading subtitle for {imdb_id}: {e}")

# Loop through each Marvel movie IMDb ID and download subtitles
for imdb_id in marvel_movie_ids:
    download_subtitle(imdb_id)

# Clean up by closing the driver
driver.quit()
