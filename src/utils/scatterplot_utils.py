from src.controller.csv_controller import CSVController
from src.enums.cell_enums import BethesdaSystemEnum


def format_items_to_scatterplot_pattern(CSV_CELLS_PATH):
    csv_cells = CSVController(CSV_CELLS_PATH, type='r')
    items_format = {}
    for bethesda in BethesdaSystemEnum:
        items_format[bethesda.name] = {}
        items_format[bethesda.name]['areas'] = []
        items_format[bethesda.name]['eccentricity'] = []

    csv_content = csv_cells.read_csv()
    for row in csv_content:
        items_format[row['class']]['areas'].append(float(row['area']))
        items_format[row['class']]['eccentricity'].append(float(row['eccentricity']))

    csv_cells.close_csv()

    return items_format
