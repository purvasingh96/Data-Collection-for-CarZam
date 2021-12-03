#!/usr/bin/env python3

"""salesScraper.py: Pulls data from all CarMax sales listings and exports to a file called salesListingsCurrent.csv."""

__author__      = "Purva Singh"
__version__ = "1.0"
__maintainer__ = "Purva Singh"
__email__ = "psingh359@gatech.edu"

import lib.csvHandler as csv
import furl
import logging
import math
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from scripts.zipcode_generator_util import zipcode_generator_util

logging.basicConfig(filename='../logs/carmax-sales-data.log', format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


baseUrl = "https://www.carmax.com/cars/api/search/run"

params = {"uri": "/cars/all","skip": 24,"take": 100, "radius": 90, "zipCode": 94014, "shipping": 20, "sort": 20, "scoringProfile": "BestMatchScoreVariant3"}

#https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fall&skip=96&take=24&zipCode=30334&radius=90&shipping=&sort=100&scoringProfile=BestMatchScoreVariant3

exportCSVFilename = 'salesListingsCurrent.csv'
allItemsForSale = []
data = {}
csv_list = []

def constructUrl():
    global baseUrl
    global params

    f = furl.furl(baseUrl)
    f.args = params
    return f.url

def extractJsonFromSeleniumSource():
    global driver
    global data

    prev_data = data

    try:
        pre = driver.find_element(by=By.TAG_NAME, value="pre").text
        data = json.loads(pre)
        prev_data = data
    except Exception as e:
        print("exception occured", e)
        return prev_data

    return data

def addEntriesToList(data):
    itemSaleList = data["items"]
    for i in range(len(itemSaleList)):
        allItemsForSale.append(itemSaleList[i])


def csv_combiner(csv_list):
    df = []
    for x in csv_list:
        data_frame = pd.read_csv(x)
        df.append(data_frame)

    final_df = pd.concat(df)
    final_df = final_df.drop_duplicates(keep='last')
    final_df.to_csv(os.path.join(os.path.dirname(__file__), "final.csv"))


if __name__ == '__main__':

        original_skip_value = params["skip"]

        driver = webdriver.Chrome()

        driver.get(constructUrl())
        # endregion

        # region Display total CarMax listings
        totalListingsToGet = extractJsonFromSeleniumSource()["totalCount"]
        print("Listings to scrape: " + str(totalListingsToGet))
        # endregion

        logging.info("STARTED Scraping " + str(totalListingsToGet) + " listings")

        for i in range(math.floor(totalListingsToGet / 1000)):
            driver.get(constructUrl())

            addEntriesToList(extractJsonFromSeleniumSource())

            time.sleep(0.4)

            params["skip"] += 1000

        params["take"] = (totalListingsToGet % 1000)

        driver.get(constructUrl())
        addEntriesToList(extractJsonFromSeleniumSource())

        final_file_name= 'vehicle_features.csv'
        csv.exportCSV(final_file_name, allItemsForSale)

        print("Exported all listings to " + exportCSVFilename)
        params["skip"] = original_skip_value

