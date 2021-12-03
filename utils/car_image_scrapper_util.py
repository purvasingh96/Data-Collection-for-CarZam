__author__      = "Purva Singh"
__version__ = "1.0"
__maintainer__ = "Purva Singh"
__email__ = "psingh359@gatech.edu"


import os
import base64

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from utils.vehicle_identification_features_scrapper_util import vehicle_identification_features_scrapper_util


"""
This class parses carmax website to extract multiple orientations of a particular car and stores those images in ./CarMaxxer/images/<car-id> folder.
"""

class car_image_scrapper_util:

    @staticmethod
    def constructUrl(card_id):
        return "https://www.carmax.com/car/"+str(card_id)

    def download_one_360_image(self, car_id, car_images_folder, idx):
        driver = webdriver.Chrome()
        driver.get(self.constructUrl(car_id))

        elem = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH,
                                                                                                "//div[@class='QSIFeedBackLink SI_ah0reLCPOi4vXLv_FeedBackLinkContainer']")))

        blob_list_new = elem.find_elements(by=By.XPATH, value="//img[@class='exterior-360-image']")
        driver.get(blob_list_new[idx].get_attribute("src"))
        driver.save_screenshot(os.path.join(car_images_folder, str(car_id) + "_"+ str(idx) + '.png'))

        driver.quit()

    def extract_360_images(self, driver, car_id):
        image_folder = os.path.join(os.path.dirname(__file__), "images")
        car_images_folder = os.path.join(image_folder, str(car_id))
        os.mkdir(car_images_folder)

        driver.get(self.constructUrl(car_id))

        elem = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH,
                                                                                                "//div[@class='QSIFeedBackLink SI_ah0reLCPOi4vXLv_FeedBackLinkContainer']")))
        blob_list = elem.find_elements(by=By.XPATH, value="//img[@class='exterior-360-image']")

        driver.close()

        for idx in range(len(blob_list)):
            self.download_one_360_image(car_id, car_images_folder, idx)

        driver.quit()


if __name__ == '__main__':

    c = car_image_scrapper_util()
    v = vehicle_identification_features_scrapper_util()

    driver = webdriver.Chrome()
    for car_id in v.return_car_ids():
        c.extract_360_images(driver, car_id)


