import argparse
import multiprocessing
import time
from conf import config
from timetable_utils import *


def arguments():
    """
    Parse command-line arguments using argparse.

    Returns:
        argparse.ArgumentParser: Argument parser object.
    """

    info = ('If any argument is not specified, default settings with timeout set to 3 minutes, preset timetable with '
            'subjects, offset set to 2 seconds and process count equal to cpu count - 1 will be used.')
    parser = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter, description=info)

    time_text = 'Sets program timeout in seconds'
    parser.add_argument('-t', '--time', '--timeout', type=int, metavar='TIME', help=time_text)

    subject_info = 'Imports subjects from specified JSON file'
    parser.add_argument('-s', '--subject', '--subjects', type=str, metavar='SUBJECT', help=subject_info)

    timetable_info = 'Imports timetable from specified CSV file'
    parser.add_argument('-i', '--input', '--timetable', type=str, metavar='INPUT', help=timetable_info)

    process_info = 'Sets how many processes should be used for generation'
    parser.add_argument('-p', '--process', '--processes', type=int, metavar='PROCESS', help=process_info)

    offset_info = 'Sets how often should generator upload to evaluate in seconds, not recommended to change'
    parser.add_argument('-o', '--offset', type=int, metavar='OFFSET', help=offset_info)

    return parser


def results(generated: multiprocessing.Value, evaluated: multiprocessing.Value, evaluated_list: list):
    """
    Returns the results of the program, including total generated variants, total evaluated variants,
    better variants than the original, and the best variant.

    Args:
       generated (multiprocessing.Value): Shared variable representing the total number of generated variants.
       evaluated (list): Shared variable representing the total number of evaluated variants.
       evaluated_list (list): List of evaluated timetable variants.

    Returns:
        results (str): Statistics of generated and evaluated timetables.
    """
    total_generated = generated.value
    total_evaluated = evaluated.value
    original_variant = evaluated_list[0][0]
    best_variants = list()

    for val in evaluated_list:
        for ttable in val:
            if ttable.points > original_variant.points:
                best_variants.append(ttable)

    if len(best_variants) == 0:
        best_variant = original_variant
    else:
        best_variants.sort(key=lambda x: x.points)
        print(best_variants)
        best_variant = best_variants[0]

    result = '<-------------------------------------------------------->'
    result += f'\nTotal generated: {total_generated}'
    result += f'\nTotal evaluated: {total_evaluated}'
    result += f'\nBetter variants than original: {len(best_variants)}'
    result += f'\nBest variant: \n{best_variant}'
    result += f'\n<-------------------------------------------------------->'

    return result


def main():
    """
    Main function to execute the program.

    Parses command-line arguments, initializes program parameters, and starts multiprocessing components.
    """

    args = arguments().parse_args()
    timeout = config.timeout
    offset = config.offset
    timetable_path = config.timetable_path
    process_count = multiprocessing.cpu_count() - 1
    subjects_path = config.subjects_path

    if args.time:
        timeout = args.time
    if args.offset:
        offset = args.offset
    if args.input:
        timetable_path = args.input
    if args.process:
        process_count = args.process
    if args.subject:
        subjects_path = args.subject

    loaded_timetable = timetable_loader.load_timetable(timetable_path)
    subjects = timetable_loader.load_subjects(subjects_path)

    manager = multiprocessing.Manager()
    versions_queue = manager.Queue()
    versions_queue.put([tuple(loaded_timetable)])
    cleared_versions_queue = manager.Queue()
    evaluated_versions = manager.list()
    total_generated = multiprocessing.Value('i', 0)
    total_evaluated = multiprocessing.Value('i', 0)
    process_list = list()

    for i in range(process_count):
        if i % 5 == 0:
            process_list.append(Generator(loaded_timetable, offset, versions_queue))
        else:
            process_list.append(Evaluator(cleared_versions_queue, evaluated_versions, subjects, total_evaluated))
    process_list.append(DuplicateCleaner(versions_queue, cleared_versions_queue, total_generated))

    pids = list()
    for process in process_list:
        process.start()
        pids.append(process.pid)

    timer = Watchdog(timeout, pids)
    timer.start()

    while timer.is_alive():
        print('Generated:', total_generated.value)
        print('Evaluated:', total_evaluated.value)
        print()
        time.sleep(2)

    for process in process_list:
        process.join()

    print(results(total_generated, total_evaluated, evaluated_versions))


if __name__ == '__main__':
    main()
