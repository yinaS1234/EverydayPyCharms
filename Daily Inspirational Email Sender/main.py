import smtplib
import random
import datetime as dt
import pytz
import time
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage



load_dotenv()  # Load environment variables from a .env file
receiver = os.getenv('RECEIVER_EMAIL')
sender = os.getenv('SENDER_EMAIL')
password = os.getenv('SENDER_PASSWORD')

now = dt.datetime.now(pytz.timezone('US/Pacific'))
print(now)
weekday = now.weekday()
print(weekday)

# setup chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

def google_image():
    # TODO 3.search and locate image tab and click
    driver.get('https://www.google.com')
    search_bar = driver.find_element(By.NAME, 'q')
    search_bar.send_keys('motivational quote')
    search_bar.send_keys(Keys.RETURN)

    try:
        images_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Images")]'))
        )
        images_tab.click()

        time.sleep(10)

        # TODO 4 extract all images and download a random image
        all_images = driver.find_elements(By.XPATH, '//img[contains(@class,"rg_i")]')
        return all_images
    except Exception as e:
        print(f'An error occurred during image search: {e}')
        return None

def send_email(filename):
    if weekday < 5:
        # choose a quote
        with open('quotes.txt') as f:
            all_quotes = f.readlines()
            quote = random.choice(all_quotes)

        # connect to SMTP server
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=sender, password=password)

            # create the MIME object
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = 'Daily Motivation'

            with open(filename, 'rb') as img_f:
                img = MIMEImage(img_f.read())

            msg.attach(MIMEText(f'Here is the daily motivation. \n\n Enjoy! \n\n {quote}', 'plain'))
            msg.attach(img)

            connection.sendmail(from_addr=sender, to_addrs=receiver,
                                msg=msg.as_string())
        print('Email Sent')

def download_image(all_images):
    if not all_images:
        print('No image found')
        driver.quit()
        return None
    else:
        chosen_image = random.choice(all_images)
        image_url = chosen_image.get_attribute('src')
        filename = 'motivational_quote_today.jpg'
        print(f'Image filename: {filename}')
        urllib.request.urlretrieve(image_url, filename)
        print('Image saved in the working directory')
        return filename

def main():
    max_retries = 2
    retries = 0
    while retries < max_retries:
        try:
            all_images = google_image()
            if all_images:
                filename = download_image(all_images)
                if filename:
                    send_email(filename)
                    break  # Success, exit the loop
        except Exception as e:
            retries += 1
            print(f'Attempt {retries} failed. Retrying... Error: {e}')
        finally:
            driver.quit()

if __name__ == '__main__':
    main()
