import csv


class Recorder:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def init(self, headers: list):
        with open(self.file_path, 'w', newline='') as f:
            # init file with headers
            f_csv = csv.writer(f)
            f_csv.writerow(headers)

    def write_row(self, row):
        with open(self.file_path, 'a', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(row)
