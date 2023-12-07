from src.utils.os_utils import OSUtils
import csv


class CSVController:
    def __init__(self, CSV_PATH, type='w'):
        self.open_csv(CSV_PATH, type)

    def __add_header_to_file(self):
        header = ['cell_id', 'area', 'compactness', 'eccentricity', 'class']
        self.insert_row(header)

    def open_csv(self, CSV_PATH, type):
        csv_exists = OSUtils.exist_file(CSV_PATH)
        self.csv_file = open(CSV_PATH, type, newline='')
        if not csv_exists:
            self.__add_header_to_file()

    def close_csv(self):
        self.csv_file.close()

    def insert_row(self, data):
        csv_write = csv.writer(self.csv_file)
        csv_write.writerow(data)

    def read_csv(self):
        return csv.DictReader(self.csv_file)
