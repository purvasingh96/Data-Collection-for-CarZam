import pandas as pd
import os
import sys

class vehicle_identification_features_scrapper_util:
    def __init__(self):
        self.columns_to_keep = ["stockNumber", "year", "make", "model", "body", "trim", "features", "exteriorColor", "vehicleSize", "types"]
        self.path_to_csv_file = os.path.join(os.path.dirname(__file__), "../vehicle_features.csv")
        self.df = pd.read_csv(self.path_to_csv_file, usecols=self.columns_to_keep)
        self.car_ids = []

    def create_row_subset(self):
        self.df.to_csv('../vehicle_identification_features.csv')

    def return_car_ids(self):
        return self.df["stockNumber"].to_list()


if __name__ == '__main__':
    c = vehicle_identification_features_scrapper_util()
    print(c.return_car_ids())

