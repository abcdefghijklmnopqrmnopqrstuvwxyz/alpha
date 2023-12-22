class Subject:
    """
    Subject Class

    Represents a subject with specific attributes such as name, classroom, teacher, storey,
    practice status, and profile subject status.
    """

    def __init__(self, name: str, classroom: str, teacher: str, storey: int, is_practice: bool, is_profile_subject: bool):
        """
        Initializes a new Subject instance.

        Args:
            name (str): The name of the subject.
            classroom (str): The classroom where the subject is taught.
            teacher (str): The teacher responsible for the subject.
            storey (int): The storey or floor where the subject is scheduled.
            is_practice (bool): Indicates whether the subject involves practical sessions.
            is_profile_subject (bool): Indicates whether the subject is a part of the student's profile.

        Raises:
            TypeError: If any of the input parameters has an incorrect type.
        """

        if (not isinstance(name, str) or not isinstance(classroom, str)
                or not isinstance(teacher, str) or not isinstance(storey, int)
                or not isinstance(is_practice, bool) or not isinstance(is_profile_subject, bool)):
            raise TypeError
        self.name = name
        self.classroom = classroom
        self.teacher = teacher
        self.storey = storey
        self.is_practice = is_practice
        self.is_profile_subject = is_profile_subject

    def __str__(self):
        """
        Returns a string representation of the Subject instance.

        Returns:
            str: A formatted string representing the subject's attributes.
        """

        return f'Subject: {self.name}, classroom: {self.classroom}, teacher: {self.teacher}, storey: {self.storey}, ' \
               f'is practise: {self.is_practice}, is profile subject: {self.is_profile_subject}'
