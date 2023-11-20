import day, clock, time
### EVERYTHING AFTER THIS WILL BE REMOVED WHEN THIS IS AN NTP SERVER ###
# deletes the last line 
def deletelastline():
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    print(LINE_UP, end=LINE_CLEAR)
    
# The delay between loops of the clock
delaytime = 0.1

# the loop to display the clock
while True:    
    ticks = clock.ticksout()
    if ticks < 100:
        ticks = "00" + "{:.2f}".format(ticks)
    elif ticks < 1000:
        ticks = "0" + "{:.2f}".format(ticks)
    
    percent_of_year = day.percent_year()
    percent_of_year = percent_of_year*100
    if percent_of_year < 10:
        percent_of_year = "00" + "{:.2f}".format(percent_of_year)
    elif percent_of_year < 100:
        percent_of_year = "0" + "{:.2f}".format(percent_of_year)
    
    deletelastline()
    print(str(percent_of_year) + ":" + str(ticks))
    time.sleep(delaytime)