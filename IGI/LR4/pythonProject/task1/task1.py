import random
from services.input_funcs import Input
from task1.serializer import Serializer


class Address:
    def __init__(self, street, house, apartment):
        self.street = street
        self.house = house
        self.apartment = apartment

    def __str__(self):
        return f"{self.street}, {self.house}, {self.apartment}"


class Task1:
    def __init__(self):
        self.data = []

    def solve(self):
        """
        Function for solving this task
        """
        self.data_intput()
        self.write_to_files()

        data1 = Serializer.deserialize_from_csv("task1.csv")
        data2 = Serializer.deserialize_from_pickle("task1.pickle")
        for item in data2:
            print(f"{item['surname']}, {item["address"]}", sep="\n")

        print("\nEnter -1 to pass function or street to show students on it:")
        street = input()
        if street != -1:
            res = [item for item in data2 if item['address'].street == street]
            for item in res:
                print(f"{item['surname']} lives on {item['address']}", sep="\n")

        print("\nEnter -1 to pass function or house number to show students in it:")
        house = Input.input_int()
        if house != -1:
            res = [item for item in data2 if item['address'].house == house]
            for item in res:
                print(f"{item['surname']} lives on {item['address']}", sep="\n")

    def write_to_files(self):
        """
        Function for writing data to files
        """
        Serializer.serialize_to_csv("task1.csv", self.data)
        Serializer.serialize_to_pickle("task1.pickle", self.data)

    def data_intput(self):
        """
        Function for entering task data
        """
        print("Enter 1 to enter data from keyboard and other number to generate 5 data items:")
        n = Input.input_int()
        if n == 1:
            print(f"Enter {5} students:")
            for i in range(5):
                print(f"Enter the surname of {i + 1} student:")
                surname = input()
                print(f"Enter the street of {i + 1} student:")
                street = Input.input_int()
                print(f"Enter the house number of {i + 1} student:")
                house = Input.input_int()
                print(f"Enter the apartment number of {i + 1} student:")
                apartment = Input.input_int()
                self.data.append({"surname": surname, "address": Address(street, house, apartment)})
        else:
            surnames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
                        "Moore", "Taylor"]
            streets = ["Main Street", "Oak Avenue", "Maple Lane", "Cedar Road", "Pine Street", "Elm Avenue",
                       "Willow Lane", "Birch Road", "Spruce Street", "Hickory Avenue"]
            for i in range(5):
                random.shuffle(surnames)
                random.shuffle(streets)
                self.data.append({"surname": surnames[0], "address":
                                 Address(streets[0], random.randint(1, 100), random.randint(1, 100))})