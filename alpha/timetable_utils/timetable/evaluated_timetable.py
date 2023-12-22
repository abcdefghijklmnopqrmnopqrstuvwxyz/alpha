class EvaluatedTimetable:
    """
    Represents an evaluated timetable with associated points and subject information.
    """

    def __init__(self, timetable: tuple, points: int, subjects: dict):
        """
        Initialize an EvaluatedTimetable object.

        Args:
            timetable (tuple): A tuple representing the timetable.
            points (int): The points/evaluation associated with the timetable.
            subjects (dict): A dictionary mapping subject IDs to Subject objects.

        Raises:
            TypeError: If the input types are not as expected.
        """

        if not (isinstance(timetable, tuple) or isinstance(points, int) or isinstance(subjects, dict)):
            raise TypeError
        self.timetable = timetable
        self.points = points
        self.subjects = subjects

    def __str__(self):
        """
        Return a formatted string representation of the EvaluatedTimetable.

        Returns:
            str: Formatted string representation of the timetable.
        """

        max_length = 0
        for subject in self.timetable:
            subject_name = self.subjects.get(subject).name if self.subjects.get(subject) is not None else " - "
            subject_length = len(subject_name)
            max_length = max(max_length, subject_length)

        rows = []
        for i in range(0, len(self.timetable), int(len(self.timetable) / 5)):
            row = self.timetable[i: i + int(len(self.timetable) / 5)]
            rows.append(row)

        formatted = []
        for row in rows:
            formatted_row = []
            for subject in row:
                subject_name = self.subjects.get(subject).name if self.subjects.get(subject) is not None else " - "
                formatted_subject = f'{subject_name :{max_length}}'
                formatted_row.append(formatted_subject)
            formatted.append(' | '.join(formatted_row))

        return f'\n'.join(formatted)
