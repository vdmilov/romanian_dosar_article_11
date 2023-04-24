import os
import time
import shutil
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import url, downloads_folder, destination_folder


# Get the current year and today
current_year = datetime.datetime.now().year
today = datetime.date.today().strftime('%Y-%m-%d')


def download_dosar_pdfs(url=url):
    # set options to open PDF externally = download them straight away
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {"plugins.always_open_pdf_externally": True})
    driver = webdriver.Chrome(options=options)

    # get the link
    driver.get(url)

    # find all the pdf download link elements
    pdf_links = driver.find_elements(By.XPATH, '//a[contains(@href, ".pdf")]')

    # loop over the pdf links and download each pdf
    for link in pdf_links:
        # click on the link to open the PDF (in our case to download it directly)
        try:
            link.click()
        except:
            pass

    # give time to finish the download
    time.sleep(20)

    # quit the driver
    driver.quit()


def move_dosar_pdfs(downloads_folder=downloads_folder, 
    destination_folder=destination_folder,
    current_year=current_year,
    today=today):

    # Loop through the files in the Downloads folder
    for file_name in os.listdir(downloads_folder):
        # Check if the file contains a year from 2010 to the current year and of pdf format
        for year in range(2010, current_year + 1):
            if str(year) in file_name and file_name.endswith('.pdf'):
                # Create file path to check for the datestamp
                file_path = os.path.join(downloads_folder, file_name)
                # Check for datestamps
                if datetime.date.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d') == today:
                    # If the file contains the year, move it to the destination folder
                    shutil.move(file_path, os.path.join(destination_folder, file_name))
                    break


def delete_dosar_pdfs(delete_folder=destination_folder):
    folder_path = delete_folder

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)