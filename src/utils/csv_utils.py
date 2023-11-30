from src.singleton.cells_singleton import CellListSingleton, Cell
import csv


def read_csv(file_path):
    cells = CellListSingleton()
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            cells.append(Cell(*line))
