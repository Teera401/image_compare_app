class CsvProvider:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv(self):
        import csv
        with open(self.file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            data = [row for row in csv_reader]
        return data
    def write_csv(self, data, fieldnames):
        import csv
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)