'''
Class for a discord-friendly calendar

load_config: loads a list of date-events from a file

add_date: adds a date to the list and file

compile_calendar: combines all added dates with loaded dates, sorts them, and outputs
'''

import datetime

class DiscordCalendar:

    def __init__(self):

        global calendar
        calendar = {}

    def load_config(self):

        file = open("calendar.txt", "r")
        filelist = file.readlines()

        keys = []
        for i in filelist:
            key = i[:10]
            key = datetime.date.fromisoformat(key).toordinal()
            keys.append(key)

        values = []
        for i in filelist:
            value = i[13:-1]
            values.append(value)

        for i in keys:
            calendar[i] = values[keys.index(i)]

        file.close()

    def add_date(self, month, day, year, event):
        
        try: month = int(month)
        except: print("month is not an integer")

        try: day = int(day)
        except: print("day is not an integer")

        try: year = int(year)
        except: print("year is not an integer")

        try: event = str(event)
        except: print("event is not a string")

        datetime_date = datetime.date(year, month, day)
        ord_date = datetime_date.toordinal()
        
        calendar[ord_date] = event


    def compile_calendar(self):

        self.load_config()

        keys = sorted(calendar)
        file = open("calendar.txt", "w+")

        o_list = []
        for i in keys:
            e = datetime.date.fromordinal(i).isoformat()
            file.write(f"{e} : {calendar[i]}\n")
            o_list.append(f"{e} : {calendar[i]}\n")

        calendar.clear()

        file.close()
        if o_list != []:
            return "".join(o_list)
        else:
            return "No Calendar Events"