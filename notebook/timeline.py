#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>
import dateparser


def parse_timeline(entry):
    entry = str(entry)
    start_month = start_year = end_month = end_year = None
    for k,v in dict(early='January - March', mid='May - September', late='October - December').items():
        entry = entry.replace(k, v)

    if '-' in entry:
        start, end = entry.split('-')
        end = dateparser.parse(end)
        start = dateparser.parse(f'{start} {end.year}')
    elif entry.isdigit():
        start = dateparser.parse(f'January {entry}')
        end = dateparser.parse(f'December {entry}')
    else:
        start = end = dateparser.parse(entry)

    return (start, end)

def display_timeline(entry):
    start, end = entry
    delta = end - start
    if start.year == end.year:
        if delta.days > 330:
            return start.year
        elif start.month == end.month:
            return start.strftime("%B %Y")
        else:
            return f'{start.strftime("%B")} - {end.strftime("%B %Y")}'
    else:
        return f'{start.strftime("%Y")} - {end.strftime("%Y")}'
