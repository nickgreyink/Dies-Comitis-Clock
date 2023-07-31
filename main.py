import datetime, sys, time
import os.path
import urllib.request
from datetime import datetime

def ut1():

    # Source of offset data in miliseconds
    data_pull_url = "https://maia.usno.navy.mil/ser7/finals2000A.daily"

    # File to save offset data download
    data_file = "data_clock.txt"

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
        if len(i) > 11:
            # getting whether I(live) or P(prediction)
            ut1_live_or_predict = i[57]
            if ut1_live_or_predict == "I":
                # getting the actual time offset data if live
                ut1_offset_milli = i[58:68]
    # converting offset into milliseconds for comparison
    return float(ut1_offset_milli)


def ticksout():

    # how many hours in a techinal flawless normal earth day
    dayhours = 24

    # how many seconds in a beat
    # divide hours in a technical day by 1000 since day is divided into 100 units
    # Multiply by 60 to convert hours to minutes
    # Multiply by sixty again to convert minutes to seconds
    # multiply by 1000 to convert seocnds to milliseconds
    beatsdaymilli = (dayhours / 1000) * 60 * 60 * 1000
    
    # Convert how many hours in a technical day into milliseconds
    dayhourmilli = dayhours * 60 * 60 * 1000

    incrament_data_refresh = None

    # get the offet ammount in milliseconds
    ut1_offset_milli = ut1()

    # split the current UTC time into hours, minuts, and seconds with milliseconds
    # assign each to their own variable
    t = time.time()
    timestamp = datetime.utcfromtimestamp(t).isoformat()
    hours = float(timestamp[11:13])
    minutes = float(timestamp[14:16])
    seconds = float(timestamp[17:])

    # get the current beat amount
    # substract offset ammount form the amount of milliseconds the make up a technical day
    offsethourmilli = dayhourmilli + ut1_offset_milli
    # use the new time to find what the how many seconds in a beat for the not perfect day
    # is by comparing it to the beat if it was a technical day: 86.4
    newbeat = (offsethourmilli * beatsdaymilli) / dayhourmilli

    # turns the utc hours, minutes, and seconds to milliseconds
    # adds the milliseconds from hour, the milliseconds from mminutes, and the milliseconds form seconds together
    # adds the ut1 offset into the seconds
    timeinmilliseconds = (hours * 60 * 60 * 1000) + (minutes * 60 * 1000) + (seconds * 1000) + ut1_offset_milli
    # divides the offset time in milliseconds by the new seconds in a beat to set what the current "time" is
    ticks = timeinmilliseconds / newbeat

    # This will tell it after how many beats to refresh the beat length
    # use this to set in amount of UTC minutes how often you want the
    # program to check for the latest offset milliseconds
    incrament_minutes = 15
    # converts those minutes to milliseconds
    incrament_amount = (incrament_minutes * 60 * 1000)/newbeat

    # check for the latest offset in milliseconds if program has never run before
    if incrament_data_refresh == None:
        ut1_offset_milli = ut1()
        incrament_data_refresh = (ticks + incrament_amount)

    # checks every so for the latest offset in milliseconds
    if float(ticks) > incrament_data_refresh:
        ut1_offset_milli = ut1()
        incrament_data_refresh += incrament_amount
    
    return ticks

### EVERYTHING AFTER THIS WILL BE REMOVED WHEN THIS IS AN NTP SERVER ###
# deletes the last line 
def deletelastline():
    sys.stdout.write("\033[F")
    
# The delay between loops of the clock
delaytime = 0.1

# the loop to display the clock
while True:    
    ticks = ticksout()
    if ticks < 100:
        ticks = "00" + "{:.2f}".format(ticks)
    elif ticks < 1000:
        ticks = "0" + "{:.2f}".format(ticks)
    
    deletelastline()
    print(str(str(ticks)))
    time.sleep(delaytime)