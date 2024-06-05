# Importing Modules
import sys
import os
import csv
import json
import pickle

class FileHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_file(self):
        raise NotImplementedError

    def save_file(self, data):
        raise NotImplementedError
    
class CSVHandler(FileHandler):
    def read_file(self):
        try:
            with open(self.filepath, 'r', newline='') as csvfile:
                reader = list(csv.reader(csvfile))
                print("\nOriginal CSV file:\n")
                for row in reader:
                    print(",".join(row))
                return reader
        except FileNotFoundError:
            print(f"File not found: {self.filepath}")
            return None

    def save_file(self, data):
        try:
            with open(self.filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
                print("\nModified CSV content saved successfully.\n")
                for row in data:
                    print(",".join(row))
                print("")
        except IOError:
            print(f"Error writing to file: {self.filepath}")

class JSONHandler(FileHandler):
    def read_file(self):
        try:
            with open(self.filepath, 'r') as jsonfile:
                data = json.load(jsonfile)
                print("\nOriginal JSON content:\n")
                print(data)
                return data
        except FileNotFoundError:
            print(f"File not found: {self.filepath}")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON.")
            return None

    def save_file(self, data):
        try:
            with open(self.filepath, 'w') as jsonfile:
                json.dump(data, jsonfile, indent=4)
                print("\nModified JSON content saved successfully.\n")
                print(data)
        except IOError:
            print(f"Error writing to file: {self.filepath}")

class Main:
    def __init__(self, source, destination, changes):
        self.source = source
        self.destination = destination
        self.changes = changes
        self.handler = self.get_handler(self.source)

    def get_handler(self, filepath):
        if filepath.endswith('.csv'):
            return CSVHandler(filepath)
        elif filepath.endswith('.json'):
            return JSONHandler(filepath)
        elif filepath.endswith('.pickle'):
            return PickleHandler(filepath)
        else:
            print('Unsupported file type.')
            return None

    def apply_changes(self, data):
        try:
            for change in self.changes:
                col, row, value = [int(x) if i < 2 else x.strip() for i, x in enumerate(change.split(","))]
                data[row][col] = value
            return data
        except (ValueError, IndexError):
            print("\nInvalid change, please retry!")
            return None

    def process(self):
        data = self.handler.read_file() if self.handler else None
        modified_data = self.apply_changes(data)
        if modified_data is not None:
            _, ext = os.path.splitext(self.destination)
            self.handler = self.get_handler(self.destination)
            if self.handler:
                self.handler.filepath = self.destination
                self.handler.save_file(modified_data)
            else:
                print("Unsupported destination file type.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage of the app:")
        print("Please type in the command in the following format with all arguments provided:")
        if (os.name) == "nt":
            print("py reader.py src_file dst_file change1 change2 change3 change4")
        else:
            print("python3 reader.py src_file dst_file change1 change2 change3 change4")
        sys.exit(1)

    src_file = sys.argv[1]
    dst_file = sys.argv[2]
    changes = sys.argv[3:]

    if not changes:
        print("No changes provided!")
        sys.exit(1)

    reader = Main(src_file, dst_file, changes)
    reader.process()