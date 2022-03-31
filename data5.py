''' Plots Serial Output From Arduino

In this case, Used for VIV sensor to output a column

Time, LbF (22 = .22 lbs)
...
...


To Setup:

    Scan the code and modify line 44 with /your/serial/port

    Example:
    "ser.port = '/dev/cu.usbmodem1101'  # Arduino serial port

    Pip install any necessary packages, most likely needed is Pyserial, matplotlib,
    numpy etc. Should tell you in the output of the code when you try to run it.


To Run:
    Have the Arduino Connected via USB, Build the code onto the device
    and DO NOT open the serial port (or it will mess things up) After ensuring the 
    serial port is closed, open a new terminal, navigate to:
    "./Code Systems/VIV/VIV/data5.py" in the eel repository, and enter the command

    "python data5.py"

    This will(should) open a plot that live updates the last 1000 data points
    from the arduino.


Further Development:
    Add button to save plot.


'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial

# initialize serial port
ser = serial.Serial()

#------------------------------------------------------

# Will Likely need to be changed for your Arduino Setup
ser.port = '/dev/cu.usbmodem1101'  # Arduino serial port
ser.baudrate = 115200              # Arduino Baud Rate

#------------------------------------------------------



ser.timeout = 10  # specify timeout when using readline()
ser.open()
if ser.is_open == True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n")  # print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []  # store trials here (n)
ys = []  # store relative frequency here
rs = []  # for theoretical probability

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # Aquire and parse data from serial port
    line = ser.readline()  # ascii
    line_as_list = line.split(b',')
    i = int(line_as_list[0])
    relProb = line_as_list[1]
    relProb_as_list = relProb.split(b'\n')
    relProb_float = float(relProb_as_list[0])
    print(i, relProb_float)
    if relProb_float< 100000:
    # Add x and y to lists
        xs.append(i)
        ys.append(relProb_float)
        rs.append(0.5)


#------------------------------------------------------
#More or less data Displayed before overwrite, 
# Bigger negative number = more data

    # Limit x and y lists to 20 items
    xs = xs[-200:]
    ys = ys[-200:]
#------------------------------------------------------



    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label="Experimental Probability")
    #ax.plot(xs, rs, label="Theoretical Probability")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('VIV Sensor Output')
    plt.ylabel('Pressure Sensor Readout')
    plt.legend()
    #plt.axis([1, None, 0, 1.1])  # Use for arbitrary number of trials
    #plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10)
plt.show()