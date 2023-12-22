import multiprocessing
from timetable_utils.timetable.evaluated_timetable import EvaluatedTimetable
from timetable_utils.evaluator.rules import *


class Evaluator(multiprocessing.Process):
    """
    A multiprocessing class for evaluating variations of timetables based on predefined rules.
    """

    def __init__(self, queue: multiprocessing.Queue, evaluated_versions: list, subjects: dict, total_evaluated: multiprocessing.Value):
        """
        Initialize an Evaluator object.

        Args:
            queue (multiprocessing.Queue): The input queue containing variations of timetables to be evaluated.
            evaluated_versions (list): The shared list to store EvaluatedTimetable objects.
            subjects (dict): A dictionary mapping subject IDs to Subject objects.
            total_evaluated (multiprocessing.Value): A shared integer value indicating the total number of evaluated variations.

        Raises:
            TypeError: If the input types are not as expected.
        """

        is_queue = hasattr(queue, 'put') and hasattr(queue, 'get')
        is_list = type(evaluated_versions).__name__
        is_int = type(total_evaluated).__name__
        if not is_queue or is_list != 'ListProxy' or not isinstance(subjects, dict) or is_int != 'Synchronized':
            raise TypeError
        super().__init__()
        self.queue = queue
        self.evaluated_versions = evaluated_versions
        self.subjects = subjects
        self.total_evaluated = total_evaluated

    def run(self):
        """
        Evaluate variations of timetables based on predefined rules and store the results in the evaluated_versions
        list.
        """

        function_list = [required_rules, own_rules]

        while True:
            timetables = self.queue.get()
            local_evaluated = list()
            good_variations = list()

            for timetable in timetables:
                points = 0

                for function in function_list:
                    points += function(timetable, self.subjects)

                local_evaluated.append(EvaluatedTimetable(timetable, points, self.subjects))
                if points > 0:
                    good_variations.append(EvaluatedTimetable(timetable, points, self.subjects))

            self.evaluated_versions.append(good_variations)
            self.total_evaluated.value += len(local_evaluated)
