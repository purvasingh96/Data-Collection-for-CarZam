# CS-6235 Real Time Embeded Systems Project: Data Collection for CarZam
An image + data web scraper build to crawl the [CarMax website](https://www.carmax.com) and store relevant information for vehicle identification projects.

# Project Overview
This repo contains code for my final project titled, "Data Collection for CarZam", for the course CS-6235. CarZam is a vehicle classification system for electronic traffic monitoring. 
This project talks about data collection for CarZam.<br><br>
It primarily requires different types of good-quality annotated vehicle images for training and classification purposes.
The CarZam data should mainly focus on images with multiple orientations,    and image annotations can contain unique features related to the vehicle such as model, type, color, year, brand, etc. 
There are two main features that this project delivers. Hence, this project provides two kinds of web scrapers:<br>

* Image Web Scraper
* Data Web Scraper

# How to run the project?

## Pre-requisites
* Make sure you have ***Python 3.7*** running on your machine.
* Other third party libraries that are required to be downloaded for the project (pandas, selenium, etc) have been mentioned in the `requirements.txt` file.
* Please refer to the following documentation on how to set-up ChromeDriver on your machine: [Setup ChromeDriver](https://chromedriver.chromium.org/getting-started)
* **First run the data web scraper and then the image web scraper.** This is because, data web scraper is used to extract all the Car stockNumbers which in turn is used to extract car images.  

## Extracting Vehicle Labels
Python script, ***car_schema_scrapper_util.py*** extract relevant data from the CarMax API. To run the same, simply run the main function of the class:<br>

### Usage
```python
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
```
<br>
The two CSV files (filtered and non-filtered) will get generated at the root directory after the data web scraper completes its crawling successfully.

## Extracting Vehicle Images 
Python script, ***car_image_scrapper_util.py*** crawls the web app to extract multiple images that cummulatively form the 360 degree view of a vehicle. In the crux, these images are an integration of multiple car images with different orientations, which is precisely what we need.

### Usage

```python
if __name__ == '__main__':

    c = car_image_scrapper_util()
    v = vehicle_identification_features_scrapper_util()

    driver = webdriver.Chrome()
    for car_id in v.return_car_ids():
        c.extract_360_images(driver, car_id)
```

`car_image_scrapper_util.py` uses a list of car's stockNumber to extract multiple images of the same car but with different orientation. To run the script, simply run the main fuction and Selenium will perform the rest of the task. <br>You can view all the images under `images/<car's stockNumber>` folder.  



