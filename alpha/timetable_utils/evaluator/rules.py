def _get_key_from_value(dictionary: dict, val):
    """
    Get the key associated with a given value in a dictionary.

    Args:
        dictionary (dict): The dictionary to search.
        val: The value to find the key for.

    Returns:
        The key associated with the given value.
    """

    for key, value in dictionary.items():
        if val == value:
            return key


def _points_for_hour(hour_number: int, value: int):
    """
    Calculate points for a specific hour based on the presence or absence of a subject.

    Args:
        hour_number (int): The hour number.
        value (int): The subject ID or None.

    Returns:
        int: The calculated points.
    """

    is_not_none = {
        0: -40,
        1: -5,
        2: 0,
        3: 20,
        4: 40,
        5: 30,
        6: 1,
        7: -20,
        8: -75,
        9: -150,
    }

    is_none = {
        0: 23,
        1: 2,
        2: -220,
        3: -155,
        4: -125,
        5: -99,
        6: -29,
        7: 15,
        8: 80,
        9: 210,
    }

    return is_none.get(hour_number) if value is None else is_not_none.get(hour_number)


def _points_for_hour_count(none_number: int, day_length: int):
    """
    Calculate points based on the number of None (free) hours in a day.

    Args:
        none_number (int): The number of None (free) hours.
        day_length (int): The total number of hours in a day.

    Returns:
        int: The calculated points.
    """

    values = {
        0: -5000,
        1: -3000,
        2: -2500,
        3: -2000,
        4: -600,
        5: 1,
        6: 80,
        7: 2,
        8: -500,
        9: -1000,
        10: -10000,
    }

    return values.get(day_length - none_number)


def required_rules(timetable: list, subjects: dict):
    """
    Evaluate variations of timetables based on required rules.

    Args:
        timetable (list): The timetable variation to be evaluated.
        subjects (dict): A dictionary mapping subject IDs to Subject objects.

    Returns:
        int: The calculated points for the given timetable.

    Note:
        1. Assign a bonus/malus to each box in the schedule for when the hour is/isn't there.
        2. It is wrong, if there is the same subject several times in one day, and not a multi-hour lesson. Exercise and theory can be done in one day, practice must not precedes theory.
        3. Going to other floor between classes is bad, to another classroom is also bad - it's on the same floor, it's not that bad.
        4. Every day one of the hours number 5, 6, 7 or 8 must be free for lunch.
        5. You should ideally study 5-6 hours a day, more is bad.
        6. If the exercise is two or three hours long, those hours must be in the same day.
        7. Mathematics and profile subjects should not be taught either in the first hour or after the lunch break.
        8. It must reflect your well-being
    """

    day_length = int(len(timetable) / 5)
    none_value = _get_key_from_value(subjects, None)
    hours = list()
    points = 0
    cycles = 0

    for hour in range(len(timetable)):
        # Clears hours list and resets cycles for every day
        if cycles == day_length:
            cycles = 0
            hours.clear()
        # Adds some points for every hour for being/not being there
        points += _points_for_hour(cycles, subjects.get(timetable[hour]))
        inside_cycle = 0
        for subject in hours:
            # Cycles through all subjects before current hour in a day
            if subjects.get(timetable[hour]) is not None and subjects.get(subject) is not None:
                # Checks if subjects are not None type (pause in timetable)
                if not subjects.get(timetable[hour]).is_practice and subjects.get(subject).is_practice:
                    # Checks if one of the subjects is practice and other is not
                    if subjects.get(timetable[hour]).name == subjects.get(subject).name:
                        # Checks if names matches
                        points -= 50
                if subjects.get(timetable[hour]).classroom != subjects.get(subject).classroom and len(hours) - 1 == inside_cycle:
                    # Checks if classrooms between 2 following hours matches or not
                    points -= 10
                    if subjects.get(timetable[hour]).storey != subjects.get(subject).storey:
                        # Checks if storeys between 2 following hours matches or not
                        points -= 10
                if subject == timetable[hour]:
                    # Checks if day contains 2 same subjects
                    if not (subjects.get(timetable[hour]).is_practice and subjects.get(subject).is_practice and len(
                            hours) - 1 == inside_cycle):
                        # Checks if  those 2 subjects are not practice following each other
                        points -= 100
            inside_cycle += 1
        cycles += 1
        # Adds every hour in a day to hours list
        hours.append(timetable[hour])
        if len(hours) == day_length:
            # Checks if hours contains all the subjects in a day
            points += _points_for_hour_count(hours.count(none_value), day_length)
            # Adds some points for number of lessons in one day
            if hours[4] and hours[5] and hours[6] and hours[7] != 0:
                # Checks if the day contains break for launch
                points -= 600
        if len(hours) == 1:
            # Check only for first hour in each day
            if subjects.get(hours[0]) is not None:
                # Checks if first hour is not None type (pause in timetable)
                if subjects.get(hours[0]).is_profile_subject:
                    # Checks if first hour is profile subject
                    points -= 55

    return points


def own_rules(timetable: list, subjects: dict):
    """
    Evaluate variations of timetables based on custom rules.

    Args:
        timetable (list): The timetable variation to be evaluated.
        subjects (dict): A dictionary mapping subject IDs to Subject objects.

    Returns:
        int: The calculated points for the given timetable.

    Note:
        1. Own rule #1, its principle must be obvious from the documentation.
        2. Own rule #2, its principle must be obvious even without the documentation.
    """

    day_length = int(len(timetable) / 5)
    hours = list()
    points = 0
    cycles = 0
    inside_cycle = 0

    for cycle in range(5):
        # Cycles from 0 to 5
        if subjects.get(timetable[cycle * day_length]) is not None:
            # Checks if subjects are not None type (pause in timetable)
            if subjects.get(timetable[cycle * day_length]).is_practice:
                # Checks if first hour in each day is practice
                points -= 49
    for hour in range(len(timetable)):
        # Clears hours list and resets cycles for every day
        if cycles == day_length:
            cycles = 0
            hours.clear()
            inside_cycle += 1
        cycles += 1
        # Adds every hour in a day to hours list
        hours.append(timetable[hour])
        if len(hours) == day_length:
            # Checks if hours contains all the subjects in a day
            for free_hour in range(5, 9):
                # Cycles through hours 5, 6, 7 and 8
                if subjects.get(timetable[free_hour + day_length * inside_cycle]) is None:
                    # Checks if one of those hours is None type (launch break)
                    if subjects.get(timetable[(free_hour + day_length * inside_cycle) + 1]) is not None:
                        # Checks if next hours is not None type (pause in timetable)
                        if subjects.get(timetable[(free_hour + day_length * inside_cycle) + 1]).name == 'TV':
                            # Checks if next hour is TV
                            points -= 69

    return points
