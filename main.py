# This script is used to scrape tweets from a specified Twitter user's profile
# and save them to a text file.

# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


# Function to scrape tweets
def scrape_tweets(username="elonmusk", scroll_times=10, output_file="user_tweets.txt"):
    """
    Scrape tweets from a specified Twitter user's profile.
    
    :param username: Twitter username to scrape (default: "X")
    :param scroll_times: Number of times to scroll the page (default: 10)
    :param output_file: File to save the scraped tweets (default: "user_tweets.txt")
    """
    # Set up Chrome options for headless browsing
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/90.0.4430.212 Safari/537.36')

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to the Twitter profile
    driver.get(f"https://twitter.com/{username}")

    # Wait for the page to load
    time.sleep(5)

    with open(output_file, 'w', encoding='utf-8') as file:
        for i in range(scroll_times):
            try:
                # List of possible selectors for tweet elements
                selectors = ['[data-testid="tweet"]', '.tweet', '.timeline-tweet']

                # Try different selectors to find tweet elements
                for selector in selectors:
                    # Wait for the presence of the selector
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        tweet_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        # Break out of the loop if any tweet elements are found
                        if tweet_elements:
                            break
                    # If the selector doesn't work, try the next one
                    except Exception as e:
                        print(f"Error: {str(e)}")
                        continue

                # Check if any tweets were found
                if not tweet_elements:
                    print("No tweets found. X might be blocking access or requiring login.")
                    break

                # Process each tweet
                for tweet in tweet_elements:
                    try:
                        # Extract tweet text
                        tweet_text = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text

                        # Try to find the date element
                        date_element = tweet.find_element(By.CSS_SELECTOR, 'time')
                        tweet_date = date_element.get_attribute('datetime')

                        # Write tweet information to file
                        file.write(f"Date: {tweet_date}\n")
                        file.write(f"Tweet: {tweet_text}\n\n---\n\n")
                    except Exception as e:
                        print(f"Error processing tweet: {str(e)}")

                # Print progress
                print(f"Processed scroll {i+1}/{scroll_times}")

                # Scroll to the bottom of the page
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)  # Wait for new content to load

            # If an error occurs, break the loop
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                break

    # Close the browser
    driver.quit()
    # Print success message
    print(f"Tweets saved to {output_file}")


# Usage example
if __name__ == '__main__':
    # Replace with the desired username
    user = 'elonmusk'
    # Replace with the desired number of scrolls
    scrolls = 100
    # Run function: scrape_tweets
    scrape_tweets(username=user, scroll_times=scrolls, output_file=f"{user}_tweets.txt")
