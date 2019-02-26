#!/usr/bin/env python
#generate weekdays
from excalibur import no_market_holidays
import sys
import datetime
import os
from excalibur import generate_holidays

__debug = bool(os.environ.get("DEBUG",None))

def date_jesus(start_str: str, end_str: str, delta_days: int = 1) -> [datetime.date]:
    start = datetime.datetime.strptime(start_str, '%Y%m%d')
    end = datetime.datetime.strptime(end_str, '%Y%m%d')
    delta = datetime.timedelta(days=delta_days)
    d = start
    weekend = set([5, 6])
    dates_input = []

    while d < end:
        if d.weekday() not in weekend:
            dates_input.append(d)
        d = d + delta

    dates_output = no_market_holidays.filter_dates(source_input = dates_input)

    if __debug:
        print("holidays:")
        print("=============================================")
        print(no_market_holidays.get_holidays(start_str[:4]))
        print("=============================================")
        print(generate_holidays.NYSEMarketHoliday(int(start_str[:4]), "NY"))
        print("=============================================")

    return dates_output

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("use format like '20150102', cmd is like:dateJesus.py [start_date] [end_date]")
    else:
        start_str=sys.argv[1]
        end_str=sys.argv[2]

        for d in date_jesus(start, end):
            print(d)

