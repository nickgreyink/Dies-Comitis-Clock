import datetime, sys, time
import os.path
import urllib.request
from datetime import datetime, timedelta
from time import strptime

def offset():

    # Source of offset data in miliseconds
    data_pull_url = "https://maia.usno.navy.mil/ser7/deltat.data"

    # File to save offset data download
    data_file = "data_day_clock.txt"

    # The format of the timestamp at the top of data.txt
    date_format = "%Y-%m-%d"

    # Check if data.txt exists
    if_exists_data = os.path.isfile(data_file)

    # If the data.txt file simply does not exist the create it
    # add the time stamp at the top
    if not if_exists_data:
        urllib.request.urlretrieve(data_pull_url, data_file)
        with open(data_file, 'r+') as file:
            content = file.read()
            file.seek(0)
            file.write(
                str(datetime.utcnow().strftime(date_format)) + "\n" + content)

    # open data.txt to get the first line
    with open(data_file) as f:
        first_line = f.readline()
            
    # if the first line does not equal today UTC date then
    # pull the file from the source
    # add the time stamp at the top
    if datetime.utcnow().strftime(date_format) != first_line.strip():
        urllib.request.urlretrieve(data_pull_url, data_file)
        with open(data_file, 'r+') as file:
            content = file.read()
            file.seek(0)
            file.write(
                str(datetime.utcnow().strftime(date_format)) + "\n" + content)

    # open data.txt and file the last line of acctual data
    # before predictions
    file = open(data_file, 'r')
    topology_list = file.readlines()

    last_offset = 0
    
    for i in topology_list:
        last_offset = i[13:20]
    # converting offset into milliseconds for comparison
    return float(last_offset)

def percent_year():

    # Source of offset data in miliseconds
    data_pull_url = "http://www.neoprogrammics.com/sun/Northern_Winter_Dates_and_Times.html"

    # File to save offset data download
    data_file = "data_day_sep.txt"

    # The format of the timestamp at the top of data.txt
    date_format = "%Y-%m-%d"

    # Check if data.txt exists
    if_exists_data = os.path.isfile(data_file)

    # If the data.txt file simply does not exist the create it
    # add the time stamp at the top
    if not if_exists_data:
        urllib.request.urlretrieve(data_pull_url, data_file)
        with open(data_file, 'r+') as file:
            content = file.read()
            file.seek(0)
            file.write(
                str(datetime.utcnow().strftime(date_format)) + "\n" + content)

    # open data.txt to get the first line
    with open(data_file) as f:
        first_line = f.readline()
            
    # if the first line does not equal today UTC date then
    # pull the file from the source
    # add the time stamp at the top
    if datetime.utcnow().strftime(date_format) != first_line.strip():
        urllib.request.urlretrieve(data_pull_url, data_file)
        with open(data_file, 'r+') as file:
            content = file.read()
            file.seek(0)
            file.write(
                str(datetime.utcnow().strftime(date_format)) + "\n" + content)

    # open data.txt and file the last line of acctual data
    # before predictions
    file = open(data_file, 'r')
    topology_list = file.readlines()
    
    for i in topology_list:
        if str(i[1:9]) == str(datetime.now().year-1) + " Dec":
            old_year = int(i[1:5])
            old_month = int(str(strptime(i[6:9],'%b').tm_mon))
            old_day = int(i[10:12])
            old_hour = int(i[20:22])
            old_minute = int(i[23:25])
            old_second = int(i[26:28])
            old_date = datetime(old_year, old_month, old_day, old_hour, old_minute, old_second)
        if str(i[1:9]) == str(int(datetime.now().year)) + " Dec":
            new_year = int(i[1:5])
            new_month = int(str(strptime(i[6:9],'%b').tm_mon))
            new_day = int(i[10:12])
            new_hour = int(i[20:22])
            new_minute = int(i[23:25])
            new_second = int(i[26:28])
            new_date = datetime(new_year, new_month, new_day, new_hour, new_minute, new_second)
            yeardiff = new_date - old_date
    seconds_to_sub = offset()
    current_now = datetime.now() + timedelta(seconds=(0-seconds_to_sub))
    currentdiff = current_now - old_date
    return currentdiff/yeardiff