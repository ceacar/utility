#!/usr/bin/env python
#generate weekdays
import no_market_holidays
import sys
import datetime
import os
import generate_holidays
debug = bool(os.environ.get("DEBUG",None))
if len(sys.argv) != 3:
    raise Exception("use format like '20150102', cmd is like:dateJesus.py [start_date] [end_date]")
else:
    start_str=sys.argv[1]
    end_str=sys.argv[2]
start = datetime.datetime.strptime(start_str, '%Y%m%d')
end = datetime.datetime.strptime(end_str, '%Y%m%d')
delta = datetime.timedelta(days=1)
d = start
weekend = set([5, 6])
dates_input = []

while d < end:
    if d.weekday() not in weekend:
        dates_input.append(d)
    d = d + delta

dates_output = no_market_holidays.filter_dates(source_input = dates_input)

if debug:
    print("holidays:")
    print("=============================================")
    print(no_market_holidays.get_holidays(start_str[:4]))
    print("=============================================")
    print(generate_holidays.NYSEMarketHoliday(int(start_str[:4]), "NY"))
    print("=============================================")


for res in dates_output:
    print(res)
