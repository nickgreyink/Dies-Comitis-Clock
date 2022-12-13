import datetime, sys, time
import os.path
import urllib.request
from datetime import datetime

def ut1():

    # source of offset data in miliseconds
    data_pull_url = "https://maia.usno.navy.mil/ser7/finals2000A.daily"

    # File ot save offset data download
    data_file = "data.txt"

    # The format of the timestamp at the top of data.txt
    date_format = "%Y-%m-%d"

    # Check if data.txt exists
    if_exists_data = os.path.isfile(data_file)

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
            
    # If it does not exists then pull data from online source
    # or if the first line does not equal today UTC date them
    # pull the file form the source
    if datetime.utcnow().strftime(date_format) != first_line.strip():
        urllib.request.urlretrieve(data_pull_url, data_file)
        with open(data_file, 'r+') as file:
            content = file.read()
            file.seek(0)
            file.write(
                str(datetime.utcnow().strftime(date_format)) + "\n" + content)

    # open datat.txt and file the last line of acctual data
    # before predictions
    file = open(data_file, 'r')
    topology_list = file.readlines()
    for i in topology_list:
        if len(i) > 11:
            # getting whether I(live) or P(prediction)
            ut1_live_or_predict = i[57]
            if ut1_live_or_predict == "I":
                # getting the actual offset data if live
                ut1_offset_milli = i[58:68]
    # converting ofset into seconds for comparison
    return float(ut1_offset_milli)


def ticksout():

    # hour many hours in a normal earth day
    dayhours = 24

    # how many seconds in a beat
    # divide hours in a day by 1000 since day is divided into 100 units
    # Multiply by 60 to convert hours to minutes
    # Multiply by sixty again to convert minutes to seconds
    beatsdaymilli = (dayhours / 1000) * 60 * 60 * 1000
    
    # Convert how many hours in a day into miliseconds
    dayhourmilli = dayhours * 60 * 60 * 1000

    incrament_data_refresh = None

    ut1_offset_milli = ut1()

    t = time.time()
    timestamp = datetime.utcfromtimestamp(t).isoformat()
    hours = float(timestamp[11:13])
    minutes = float(timestamp[14:16])
    seconds = float(timestamp[17:])

    offsethourmilli = dayhourmilli + ut1_offset_milli
    newbeat = (offsethourmilli * beatsdaymilli) / dayhourmilli

    # turns the utc hours and minutes to seconds
    # adds the seconds from hour and the seconds fro mminutes to seconds
    # adds the ut1 offset into the seconds
    timeinmilliseconds = (hours * 60 * 60 * 1000) + (minutes * 60 * 1000) + (seconds * 1000) + ut1_offset_milli        
    ticks = timeinmilliseconds / newbeat

    # 900 is the amount of seconds in 15 minutes
    # This will tell it after how many beats to refresh the beat length
    incrament_minutes = 15
    incrament_amount = (incrament_minutes * 60 * 1000)/newbeat

    # add the utc date time stamp on the data.txt file if the program has vever run before
    if incrament_data_refresh == None:
        ut1_offset_milli = ut1()
        incrament_data_refresh = (ticks + incrament_amount)

    # checks every so often to determin if the time stamp needs to be updated
    if float(ticks) > incrament_data_refresh:
        ut1_offset_milli = ut1()
        incrament_data_refresh += incrament_amount
    
    return ticks

### EVERYTHING AFTER THIS WILL BE REMOVED WHEN THIS IS AN NTP SERVER ###
# deletes the last line 
def deletelastline():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    
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
    print(ticks)
    time.sleep(delaytime)