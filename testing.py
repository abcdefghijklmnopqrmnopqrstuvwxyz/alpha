import multiprocessing
import time
import unittest
import conf.config
from timetable_utils import *
from timetable_utils.evaluator.rules import required_rules, own_rules
from timetable_utils.timetable.evaluated_timetable import EvaluatedTimetable
from timetable_utils.timetable.subject import Subject


class TestTimetableModule(unittest.TestCase):
    """Test cases for the Timetable module."""

    def test_loader(self):
        """Test the timetable loader function."""
        with self.assertRaises(Exception):
            timetable_loader.load_timetable('a')

        data = timetable_loader.load_subjects(conf.config.subjects_path)
        self.assertIsNotNone(data)

    def test_subject(self):
        """Test the Subject class."""
        with self.assertRaises(TypeError):
            Subject('a', 'a', 'a', '1', True, False)

        s = Subject('M', '1b', 'Teacher', 4, True, False)
        self.assertEqual(s.classroom, '1b')
        self.assertTrue(s.is_practice)

    def test_evaluated_subject(self):
        """Test the EvaluatedTimetable class."""
        with self.assertRaises(TypeError):
            EvaluatedTimetable([1, 2, 3, 4, 5], 100, {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})

        e = EvaluatedTimetable((1, 2, 3, 4, 5), 100, {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
        self.assertEqual(e.subjects.get(e.timetable[2]), 'c')


class TestGeneratorModule(unittest.TestCase):
    """Test cases for the Generator module."""

    def test_duplicate_cleaner(self):
        """Test the DuplicateCleaner class."""
        q1 = multiprocessing.Manager().Queue()
        q2 = multiprocessing.Manager().Queue()
        g = multiprocessing.Value('i', 0)
        d = DuplicateCleaner(q1, q2, g)

        q1.put([(1, 2), (2, 3)])
        q1.put([(2, 2), (4, 3)])
        q1.put([(1, 2), (2, 2)])
        d.start()
        time.sleep(1)
        d.kill()

        self.assertEqual(g.value, 4)
        self.assertEqual(q2.qsize(), 3)

        lst = list()

        for i in range(q2.qsize()):
            v = q2.get()
            for val in v:
                lst.append(val)

        self.assertEqual(len(lst), 4)

    def test_generator(self):
        """Test the Generator class."""
        tt = [1, 2, 3, 4, 5]
        q1 = multiprocessing.Manager().Queue()
        g = Generator(tt, 1, q1)

        g.start()
        time.sleep(1.5)
        g.kill()

        lst = list()
        for i in range(q1.qsize()):
            v = q1.get()
            for val in v:
                lst.append(val)

        self.assertGreater(len(lst), 50000)

        with self.assertRaises(TypeError):
            Generator(tt, 'a', q1)


def loop():
    while True:
        pass


class TestWatchdogModule(unittest.TestCase):
    """Test cases for the Watchdog module."""

    def test_watchdog(self):
        """Test the Watchdog class."""
        process = multiprocessing.Process(target=loop)
        process.start()
        lst = [process.pid]

        watchdog = Watchdog(1, lst)
        watchdog.start()

        time.sleep(1.2)

        self.assertFalse(process.is_alive())

        time.sleep(0.2)
        self.assertFalse(watchdog.is_alive())

        with self.assertRaises(TypeError):
            Watchdog(1, (123, 456))


class TestEvaluatorModule(unittest.TestCase):
    """Test cases for the Evaluator module."""

    def test_evaluator(self):
        """Test the Evaluator class."""
        q1 = multiprocessing.Manager().Queue()
        g = multiprocessing.Value('i', 0)
        first = (15, 15, 2, 3, 1, 0, 19, 19, 0, 0,
                 1, 9, 13, 13, 5, 7, 0, 8, 0, 0,
                 10, 2, 6, 6, 7, 1, 12, 0, 0, 0,
                 14, 1, 10, 18, 4, 2, 16, 0, 0, 0,
                 0, 11, 11, 5, 8, 17, 17, 0, 0, 0,)

        second = (15, 19, 2, 3, 1, 0, 15, 19, 0, 0,
                  0, 9, 13, 13, 5, 7, 0, 8, 0, 0,
                  0, 2, 0, 0, 0, 1, 12, 0, 0, 0,
                  0, 1, 10, 0, 4, 2, 0, 0, 0, 0,
                  0, 11, 11, 0, 0, 0, 17, 0, 0, 0,)

        q1.put([first, second])
        lst = multiprocessing.Manager().list()
        subs = timetable_loader.load_subjects(conf.config.subjects_path)

        e = Evaluator(q1, lst, subs, g)
        e.start()
        time.sleep(1)

        self.assertEqual(len(lst), 1)
        self.assertEqual(g.value, 2)

        e.kill()

        with self.assertRaises(TypeError):
            Evaluator(q1, list(), subs, g)

    def test_rules(self):
        """Test the rule evaluation functions."""
        tt = (15, 15, 2, 3, 1, 0, 19, 19, 0, 0,
              1, 9, 13, 13, 5, 7, 0, 8, 0, 0,
              10, 2, 6, 6, 7, 1, 12, 0, 0, 0,
              14, 1, 10, 18, 4, 2, 16, 0, 0, 0,
              0, 11, 11, 5, 8, 17, 17, 0, 0, 0,)
        required_points = 1154

        subs = timetable_loader.load_subjects(conf.config.subjects_path)
        self.assertIsNotNone(subs)

        computed = required_rules(tt, subs) + own_rules(tt, subs)
        self.assertAlmostEqual(computed, required_points)


if __name__ == '__main__':
    unittest.main()
