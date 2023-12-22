# Timetable Evaluation

This project provides functionality for generating, evaluating, and cleaning variations of timetables using multiprocessing.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Inputs](#inputs)
- [Other](#Other)

## Introduction

This project consists of several modules for working with timetables, including:

- **Generator**: Generates shuffled variations of a given timetable.
- **Evaluator**: Evaluates timetable variations based on predefined and custom rules.
- **DuplicateCleaner**: Removes duplicate variations from the generated timetables.
- **Watchdog**: Monitors all other processes and kills them after timeout.

## Features

- Multi-processing support for efficient timetable generation and evaluation.
- Customizable evaluation rules to suit specific requirements.
- Duplicate variation cleaning to ensure unique timetables.
- Highly scalable, choice of your own settings.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/abcdefghijklmnopqrmnopqrstuvwxyz/alpha.git

2. Enter folder with program:

   ```bash
   cd ./alpha

## Usage

1. Show program help

   ```bash
   python{<version>} main.py -h

2. Run program

   ```bash
   python{<version>} main.py {<parameters>}
   ```

   (Replace version and parameters with your actual values)

3. Output

   After set up time runs out, final output with statistics will be shown containing:
      - Total generated timetables 
      - Total evaluated timetables
      - Timetable count with better score than input
      - Best timetable evaluated 

## Inputs

1. Subjects

   Program allows you to customize inputs such as timetable or subjects

   To use your own timetable, you needs first to make list of subjects in JSON by program standards:

   ```bash
   "{<number>}": {
    "name": "{<string>}",
    "classroom": "{<string>}",
    "teacher": "{<string>}",
    "storey": {<number>},
    "is_practice": {<True/False>},
    "is_profile_subject": {<True/False>}
   },
   ```

   Where you replace placeholders with actual values
   
   If you wints to make free hour, use this:

   ```bash
   "{<number>}": null,
   ```

   Where you replace number with actual value

2. Timetable

   Once your subjects sheel is ready, you can make simple timetable in CSV format, for example:

   ```bash
   15, 15, 2, 3, 1, 0, 19, 19, 0, 0
   1, 9, 13, 13, 5, 7, 0, 8, 0, 0
   10, 2, 6, 6, 7, 1, 12, 0, 0, 0
   14, 1, 10, 18, 4, 2, 16, 0, 0, 0
   0, 11, 11, 5, 8, 17, 17, 0, 0, 0
   ```

   Where each number represents subject from previous section

## Other

1. License

   This program is not licensed in any way, feel free to use as you want.
