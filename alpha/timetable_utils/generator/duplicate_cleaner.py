import multiprocessing


class DuplicateCleaner(multiprocessing.Process):
    """
    A multiprocessing class for removing duplicate variations from a queue.
    """

    def __init__(self, queue: multiprocessing.Queue, cleared_queue: multiprocessing.Queue, total_generated: int):
        """
        Initialize a DuplicateCleaner object.

        Args:
            queue (multiprocessing.Queue): The input queue containing variations to be processed.
            cleared_queue (multiprocessing.Queue): The output queue containing unique variations.
            total_generated (multiprocessing.Value): A shared integer value indicating the total number of unique variations.

        Raises:
            TypeError: If the input types are not as expected.
        """

        is_queue = hasattr(queue, 'put') and hasattr(queue, 'get')
        is_cleared_queue = hasattr(cleared_queue, 'put') and hasattr(cleared_queue, 'get')
        is_int = type(total_generated).__name__
        if not is_queue or not is_cleared_queue or is_int != 'Synchronized':
            raise TypeError
        super().__init__()
        self.queue = queue
        self.cleared_queue = cleared_queue
        self.total_generated = total_generated

    def run(self):
        """
        Overrides the run method of multiprocessing.Process.

        Remove duplicate variations from the input queue and update the output queue and total_generated count.
        """
        unique_variations = set()
        while True:
            variations = self.queue.get()
            original_list = list()
            for lst in variations:
                if lst not in unique_variations:
                    original_list.append(lst)
                    unique_variations.add(lst)
            self.total_generated.value = len(unique_variations)
            self.cleared_queue.put(original_list)
