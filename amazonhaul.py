import time
import winsound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- CONFIGURATION ---
HAUL_URL = "https://www.amazon.com/haul"
TARGET_KEYWORDS = ["flash deal", "flash sale", "50% off", "sitewide sale"]
CHECK_INTERVAL = 3600  # Checks every 3600 seconds (1 hour)

def setup_browser():
    """Configures a headless browser to bypass basic bot detection."""
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Runs invisibly in the background
    # Faking a standard user agent to avoid immediate Amazon blocks
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=chrome_options)

def check_haul_for_sales():
    print(f"Checking Amazon Haul for sales at {time.ctime()}...")
    driver = setup_browser()
    
    try:
        driver.get(HAUL_URL)
        time.sleep(5) # Wait for Amazon's JavaScript to load the page content
        
        # Grab all the visible text on the page and convert it to lowercase
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        
        for keyword in TARGET_KEYWORDS:
            if keyword in page_text:
                print(f"\n ALERT! Keyword '{keyword}' found on Amazon Haul!")
                print(f"Check it out here: {HAUL_URL}\n")
                
                # Play an alert sound 
                # (Mac users: comment out winsound and use os.system('afplay /System/Library/Sounds/Glass.aiff'))
                winsound.Beep(1000, 2000) 
                return True
                
        print("No flash sales detected this time.")
        return False
        
    except Exception as e:
        print(f"An error occurred (Amazon might have blocked the script): {e}")
        return False
        
    finally:
        # Always close the browser to free up system memory
        driver.quit()

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("Starting the Amazon Haul Flash Sale Tracker...")
    while True:
        sale_found = check_haul_for_sales()
        if sale_found:
            # Pause the script for 4 hours if a sale is found to avoid spamming alerts
            time.sleep(14400) 
        else:
            time.sleep(CHECK_INTERVAL)
