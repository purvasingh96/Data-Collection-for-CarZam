from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
from collections import defaultdict
from os.path import exists

class zipcode_generator_util:
    def __init__(self):
        self.zipcode_list = []
        self.states_json_file = open(os.path.join(os.path.dirname(__file__), "states.json"))
        self.usa_states = json.load(self.states_json_file)

    def constructUrl(self, state):
        return "https://www.carmax.com/stores/search?keyword=" + str(state)

    def extract_valid_zipcodes_for(self, state):
        driver = webdriver.Chrome()
        driver.get(self.constructUrl(state))

        carmax_locations = driver.find_elements(By.XPATH, value="//div[@class='kmx-typography--body-2']")
        for idx in range(len(carmax_locations)):
            self.zipcode_list.append(carmax_locations[idx].text.split(" ")[-1].strip())

        driver.quit()

    def return_dict(self):
        return self.zipcode_list

    def generate_valid_zipcodes(self):
        for state in self.usa_states["states"]:
            self.extract_valid_zipcodes_for(state)
        return self.zipcode_list

    def cache_zipcodes(self):
        zipcode_file_path = os.path.join(os.path.dirname(__file__), "zipcodes.json")
        if os.stat(zipcode_file_path).st_size == 0:
            zipcode_dict = {
                "zipcodes": self.generate_valid_zipcodes()
            }
            print(zipcode_dict)
            json_object = json.dumps(zipcode_dict)

            with open(zipcode_file_path, 'w') as out_file:
                out_file.write(json_object)


if __name__ == '__main__':
    c = zipcode_generator_util()
    c.cache_zipcodes()








