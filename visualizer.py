from pressure import excel 
import numpy as np
import matplotlib.pyplot as plt
import pygal
import pandas as pd
import matplotlib.dates as mdates
from numpy import *
import math


##################### Two dimensional plot Scatter_hist#######################
# y = excel.df.Upper
# x = excel.df.Down

# def scatter_hist(x, y, ax, ax_histx, ax_histy):
#     # no labels
#     ax_histx.tick_params(axis="x", labelbottom=False)
#     ax_histy.tick_params(axis="y", labelleft=False)

#     # the scatter plot:
#     ax.scatter(x, y, color='#CDCECE')

#     # now determine nice limits by hand:
#     binwidth = 1
#     xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
#     lim = (int(xymax/binwidth) + 1) * binwidth

#     # 40 the bottom limit
#     bins = np.arange(40, lim + binwidth, binwidth)
#     ax_histx.hist(x, bins=bins, color='#C76957')
#     ax_histy.hist(y, bins=bins, orientation='horizontal', color='#C76957')

# # definitions for the axes
# left, width = 0.1, 0.65
# bottom, height = 0.1, 0.65
# spacing = 0.005

# rect_scatter = [left, bottom, width, height]
# rect_histx = [left, bottom + height + spacing, width, 0.2]
# rect_histy = [left + width + spacing, bottom, 0.2, height]

# # start with a square Figure
# fig = plt.figure(figsize=(8, 8))

# ax = fig.add_axes(rect_scatter)
# ax_histx = fig.add_axes(rect_histx, sharex=ax)
# ax_histy = fig.add_axes(rect_histy, sharey=ax)

# # use the previously defined function
# scatter_hist(x, y, ax, ax_histx, ax_histy)

# plt.show()


##################### Pulse Overall ##########################################
# var = excel.df.Pulse
# time = excel.df.Date

# fig, ax = plt.subplots()

# ax.plot(time, var, 'y', color='#B6B63F', marker='.',
#  	linewidth=0)

# ax.set(xlabel='Date', ylabel='Pulse',
#        title='Pulse')
# ax.grid()

# plt.show()


##################### Upper Overall ##########################################
# var = excel.df.Upper
# time = excel.df.Date

# fig, ax = plt.subplots()

# ax.plot(time, var, 'y', color='#41913D', marker='.',
# 	linewidth=0)

# ax.set(xlabel='Date', ylabel='Upper',
#        title='Upper Pressure')
# ax.grid()

# plt.show()


##################### Down Overall ###########################################
# var = excel.df.Down
# time = excel.df.Date

# fig, ax = plt.subplots()

# ax.plot(time, var, 'y', color='#518BBF', marker='.',
# 	linewidth=0)

# ax.set(xlabel='Date', ylabel='Down',
#        title='Down Pressure')
# ax.grid()

# plt.show()


##################### Time of Measurements ###################################
x = excel.df.Date
y = excel.df.Time

plt.title('Time of pressure measurement')
plt.xlabel('Date')
plt.ylabel('Time')

plt.plot(x, y, linestyle='none', marker='.')

# make time human readable from falsedate+time
xformatter = mdates.DateFormatter('%H:%M')
plt.gcf().axes[0].yaxis.set_major_formatter(xformatter)

s = plt.gca().xaxis
locator = mdates.MonthLocator()  # every month
s.set_major_locator(locator)

plt.grid()
plt.show()


##################### S and D pressure in one plot ###########################
# time = excel.df.Date
# down = excel.df.Down
# upper = excel.df.Upper

# fig, ax = plt.subplots()

# ax.plot(time, down, color='#448AB1', marker=7, markersize=7,
# 	linewidth=0)
# ax.plot(time, upper, color='#B14C44', marker=6, markersize=7,
# 	linewidth=0)

# ax.set(xlabel='Date', ylabel='Pressure',
#        title='Systolic and Diastolic pressure correlation')
# ax.grid()

# plt.show()


##################### D, S and pulse in one plot #############################
# time = excel.df.Date
# down = excel.df.Down
# upper = excel.df.Upper
# pulse = excel.df.Pulse

# fig, ax = plt.subplots()

# ax.plot(time, down, color='#448AB1', marker=7, markersize=7,
# 	linewidth=0)
# ax.plot(time, upper, color='#B14C44', marker=6, markersize=7,
# 	linewidth=0)
# ax.plot(time, pulse, color='#CFC843', linewidth=1.5)

# ax.set(xlabel='Date', ylabel='Pressure/Pulse',
#        title='Systolic and Diastolic pressure and Pulse correlation')
# ax.grid()

# plt.show()
