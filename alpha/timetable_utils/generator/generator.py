import multiprocessing
import random
import time


class Generator(multiprocessing.Process):
    """
    A multiprocessing class for generating shuffled variations of a timetable.

    Note: The run method continuously generates shuffled variations at regular intervals and puts them into the
    output queue.
    """

    def __init__(self, timetable: list, offset: int, queue: multiprocessing.Queue):
        """
        Initialize a Generator object.

        Args:
            timetable (list): The original timetable to generate variations from.
            offset (int): The time interval (in seconds) between generating and putting variations into the queue.
            queue (multiprocessing.Queue): The output queue to store generated variations.

        Raises:
            TypeError: If the input types are not as expected.
        """

        is_queue = hasattr(queue, 'put') and hasattr(queue, 'get')
        if not isinstance(timetable, list) or not isinstance(offset, int) or not is_queue:
            raise TypeError
        super().__init__()
        self.timetable = timetable
        self.offset = offset
        self.queue = queue

    def run(self):
        """
        Overrides the run method of multiprocessing.Process.

        Generate shuffled variations of the timetable and put them into the output queue at regular intervals.
        """

        versions = list()
        timer = time.time()
        while True:
            versions.append(self.generate_shuffled_list())
            if time.time() > timer + self.offset:
                timer += self.offset * 2
                self.queue.put(versions)
                versions.clear()

    def generate_shuffled_list(self):
        """
        Generate a shuffled version of the original timetable.

        Returns:
            tuple: A tuple representing a shuffled version of the timetable.
        """

        shuffled_list = self.timetable.copy()
        random.shuffle(shuffled_list)
        return tuple(shuffled_list)
