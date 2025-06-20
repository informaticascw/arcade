import json, os, datetime
from util.constants import Constants

def mergeDicts(d1, d2):
    """Merge 2 dicts together into one using recursion, will override duplicates in the first dict.

    Args:
        d1 (dict): Dictionary to merge.
        d2 (dict): With this dict.
    """
    for k in set(d1.keys()).union(d2.keys()):
        if k in d1 and k in d2:
            if isinstance(d1[k], dict) and isinstance(d2[k], dict):
                yield(k, dict(mergeDicts(d1[k], d2[k])))
            else: yield(k, d2[k])
        elif k in d1: yield(k, d1[k])
        else: yield(k, d2[k])

class PogDict:
    def __init__(self, defDict={}, fileName="data", autoSaveInterval=300) -> None:
        """Creates a data object that can be altered from anywhere and will be written to a file. Uses JSON formatting.

        Args:
            defDict (dict, optional): Default dict, define what keys will be stores and their according default values. Defaults to {}.
            fileName (str, optional): Name of the json file. Defaults to "data".
            autoSaveInterval (int, optional): Interval in which the data will be auto written to file, in seconds. Defaults to 300.
        """
        self.fileName = fileName + ".json"
        self.defDict = defDict
        self.autoSaveInterval = autoSaveInterval
        try:
            with open(self.fileName, "r") as f:
                self.data = dict(mergeDicts(defDict, json.load(f)))
        except:
            with open(self.fileName, "w") as f:
                self.data = defDict
                json.dump(defDict, f, indent=4)
        self.save()

    def save(self) -> None:
        """Function to manualy save the data object to the json file."""
        try:
            os.remove(self.fileName)
            with open(self.fileName, "w") as f:
                    json.dump(dict(mergeDicts(self.defDict, self.data)), f, indent=4)
            print(f"{Constants.CNSL_DATA}[DATA] Data saved!{Constants.CNSL_RESET}")
        except:
            print(f"{Constants.CNSL_DATA}[DATA] Failed to save the data!{Constants.CNSL_RESET}")

    def autoSave(self) -> None:
        """Start the auto saving sequence (Won't stop till system exits."""
        lastSave = datetime.datetime.now().timestamp()
        while True:
            now = datetime.datetime.now().timestamp()
            if now - lastSave >= self.autoSaveInterval:
                print(f"{Constants.CNSL_DATA}[DATA] Auto saved the data!{Constants.CNSL_RESET}")
                self.save()
                lastSave = now

    def setValue(self, key:str, value) -> None:
        """Set a value in the data.

        Args:
            key (str): Key of the value you want to set.
            value (any): Value to be paired to the key.
        """
        self.data[key] = value

    def getValue(self, key:str):
        """Fetch a value of the data

        Args:
            key (str): Ket to the value you want to fetch.

        Returns:
            any: Value belonging to the given key
        """
        return self.data[key]

# I am too late with commenting this, no clue as to wtf is going on in this file. But it works, so we don't question it.

data = PogDict({
    "highscores": {}
})