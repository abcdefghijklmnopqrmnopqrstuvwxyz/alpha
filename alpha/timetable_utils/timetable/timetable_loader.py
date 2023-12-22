import csv
import json
from timetable_utils.timetable.subject import Subject


def load_timetable(timetable_path: str):
    """
    Load a timetable from a CSV file.

    Args:
        timetable_path (str): The path to the CSV file containing the timetable.

    Returns:
        list: A list representing the timetable.

    Raises:
        Exception: If there is an error loading the timetable or if the file format is invalid.
    """

    timetable = list()
    try:
        with open(timetable_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                for num in row:
                    timetable.append(int(num))
        if len(timetable) % 5 != 0:
            raise Exception('Invalid timetable file format')
    except:
        raise Exception(f'An error occurred trying to load file: "{timetable_path}"')

    return timetable


def load_subjects(subjects_path: str):
    """
    Load subjects from a JSON file.

    Args:
        subjects_path (str): The path to the JSON file containing the subjects.

    Returns:
        dict: A dictionary mapping subject IDs to Subject objects.

    Raises:
        Exception: If there is an error loading the subjects or if the file format is invalid.
    """

    subjects = dict()
    try:
        with open(subjects_path, 'r') as file:
            data = json.load(file)
            for row in data.items():
                if row[1] is not None:
                    subjects[int(row[0])] = Subject(**row[1])
                else:
                    subjects[int(row[0])] = None
    except:
        raise Exception(f'An error occurred trying to load file: "{subjects_path}"')

    return subjects
