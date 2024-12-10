from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless=new")  # Optional: Run in headless mode
    return webdriver.Chrome(options=options)

driver = create_driver()
driver.maximize_window()

# Target URL
url = "https://nami-nami.ee/retseptid"
driver.get(url)

# Wait helper
wait = WebDriverWait(driver, 10)

# Set for storing unique recipe links
recipe_links = set()

# Function to extract recipe links
def extract_links():
    for a_tag in driver.find_elements(By.CSS_SELECTOR, "a[href^='/retsept/']"):
        recipe_links.add("https://nami-nami.ee" + a_tag.get_attribute("href"))

# Main loop to click the "Vaata veel" button and extract links
while True:
    try:
        # Wait for the "Vaata veel" button to appear
        load_more_button = wait.until(EC.element_to_be_clickable((By.ID, "more_latest")))
        
        # Scroll to the button and click it
        ActionChains(driver).move_to_element(load_more_button).perform()
        driver.execute_script("arguments[0].click();", load_more_button)

        # Wait briefly for new content to load
        time.sleep(2)

        # Extract links after loading more content
        extract_links()
    except Exception as e:
        print("No more 'Vaata veel' button or an error occurred:", e)
        break

# Final extraction after scrolling completes
extract_links()

# Print the collected links
file_name = "naminami_links.txt"
with open(file_name, "w", encoding="utf-8") as file:
    for link in sorted(recipe_links):
        file.write(link + "\n")

# Close the WebDriver
driver.quit()
