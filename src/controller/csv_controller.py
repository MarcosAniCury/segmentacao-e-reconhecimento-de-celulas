from src.utils.os_utils import OSUtils
import csv
import os


class CSVController:
    csv_file = None

    def __add_header_to_file(self):
        header = ['cell_id', 'area', 'compactness', 'eccentricity']
        self.insert_row(header)

    def open_csv(self, CSV_PATH):
        csv_exists = OSUtils.exist_file(CSV_PATH)
        self.csv_file = open(os.path.join(CSV_PATH), 'w', newline='')
        if not csv_exists:
            self.__add_header_to_file()

    def close_csv(self):
        self.csv_file.close()

    def insert_row(self, data):
        csv_write = csv.writer(self.csv_file)
        csv_write.writerow(data)
