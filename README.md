# Timetable Evaluation

This project provides functionality for generating, evaluating, and cleaning variations of timetables using multiprocessing.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
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
   cd alpha

## Usage

1. Show program help

   ```bash
   python{version} main.py -h

2. Run program

   ```bash
   python{version} main.py <parameters>

3. Output

   After set up time runs out, final output with statistics will be shown containing:
      - Total generated timetables 
      - Total evaluated timetables
      - Timetable count with better score than input
      - Best timetable evaluated 

## Other

1. License

   This program is not licensed in any way, feel free to use as you want.
