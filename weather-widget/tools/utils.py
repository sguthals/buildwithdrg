import datetime

date_str_to_ordinal = lambda s: datetime.date(int(s.split("-")[0]), int(s.split("-")[1]), int(s.split("-")[2])).toordinal()
date_str_to_date = lambda s: datetime.date(int(s.split("-")[0]), int(s.split("-")[1]), int(s.split("-")[2]))
celsius_to_fahrenheit = lambda x: "{}".format(int((x * 1.8) + 32))