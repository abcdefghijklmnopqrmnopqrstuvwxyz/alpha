# Timetable Evaluation

This project provides functionality for generating, evaluating, and cleaning variations of timetables using multiprocessing.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

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

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/timetable-evaluation.git
   cd timetable-evaluation
