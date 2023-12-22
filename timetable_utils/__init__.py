"""
Module Imports

This module imports various classes and modules from the timetable_utils package for use in the main program.

- Watchdog: Monitors the execution time of processes.
- DuplicateCleaner: Removes duplicate timetable variants.
- Evaluator: Evaluates the quality of timetable variants.
- Generator: Generates new timetable variants.
- timetable_loader: Loads timetable data from external sources.
"""

from timetable_utils.watchdog.watchdog import Watchdog
from timetable_utils.generator.duplicate_cleaner import DuplicateCleaner
from timetable_utils.evaluator.evaluator import Evaluator
from timetable_utils.generator.generator import Generator
from timetable_utils.timetable import timetable_loader
