import csv


class Config:
    def __init__(self, path):
        self._data = {}
        try:
            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    self._data[row[0]] = row[1]
        except FileExistsError:
            print("Config: No such file.")
        except IndexError:
            print("Config: Incorrect file structure.")

        self.commands = [("start", "Почати працю з ботом"), ("support", "Допомога стосовно бота"),
                         ("search", "Пошук сховища"), ("important", "Важлива інформація")]

    def get(self, key):
        if self._data.get(key):
            return self._data[key]
        print(f"Config: no such config ({key})")
