import csv
import pickle


class Serializer:

    @staticmethod
    def serialize_to_csv(file_path, data):
        """
        Serializes data to csv file
        """
        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        except FileNotFoundError:
            print("File not found.")

    @staticmethod
    def deserialize_from_csv(file_path):
        """
        Deserializes data from csv file
        """
        data = list()
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
            return data
        except FileNotFoundError:
            print("File not found.")
            return None

    @staticmethod
    def serialize_to_pickle(file_path, data):
        """
        Serializes data to pickle file
        """
        try:
            with open(file_path, 'wb') as file:
                pickle.dump(data, file)
        except FileNotFoundError:
            print("File not found.")

    @staticmethod
    def deserialize_from_pickle(file_path):
        """
        Deserializes data from pickle file
        """
        try:
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
            return data
        except FileNotFoundError:
            print("File not found.")
            return None
