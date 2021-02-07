from pressure import excel 
import numpy as np
import matplotlib.pyplot as plt
import pygal
import pandas as pd
<<<<<<< HEAD
import matplotlib.dates as mdates
=======
>>>>>>> 1c4491f72963f1a7e0a09f1b407d9107e6f32d4c

##################### Two dimensional plot Scatter_hist#######################
y = excel.df.Upper
x = excel.df.Down

def scatter_hist(x, y, ax, ax_histx, ax_histy):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    ax.scatter(x, y, color='#CDCECE')

    # now determine nice limits by hand:
    binwidth = 1
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth) + 1) * binwidth

    # 40 the bottom limit
    bins = np.arange(40, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=bins, color='#C76957')
    ax_histy.hist(y, bins=bins, orientation='horizontal', color='#C76957')

# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
spacing = 0.005

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom + height + spacing, width, 0.2]
rect_histy = [left + width + spacing, bottom, 0.2, height]

# start with a square Figure
fig = plt.figure(figsize=(8, 8))

ax = fig.add_axes(rect_scatter)
ax_histx = fig.add_axes(rect_histx, sharex=ax)
ax_histy = fig.add_axes(rect_histy, sharey=ax)

# use the previously defined function
scatter_hist(x, y, ax, ax_histx, ax_histy)

plt.show()


##################### Pulse Overall #####################################
# var = excel.df.Pulse
# time = excel.df.Date

# fig, ax = plt.subplots()

# ax.plot(time, var, 'y', color='#B6B63F', marker='.',
#  	linewidth=0)

# ax.set(xlabel='Date', ylabel='Pulse',
#        title='Pulse')
# ax.grid()

# plt.show()


<<<<<<< HEAD
##################### Upper Overall #####################################
# var = excel.df.Upper
# time = excel.df.Date

# fig, ax = plt.subplots()

# ax.plot(time, var, 'y', color='#41913D', marker='.',
# 	linewidth=0)

# ax.set(xlabel='Date', ylabel='Upper',
#        title='Upper Pressure')
# ax.grid()

# plt.show()


##################### Down Overall #####################################
# var = excel.df.Down
# time = excel.df.Date

# fig, ax = plt.subplots()

# ax.plot(time, var, 'y', color='#518BBF', marker='.',
# 	linewidth=0)

# ax.set(xlabel='Date', ylabel='Down',
#        title='Down Pressure')
# ax.grid()

# plt.show()
=======
##################### THIRD PLOT ##############################
df = pd.DataFrame({'x': excel.df.Date, 'y': excel.df.Time })


plt.plot('x', 'y', data=df, linestyle='none', marker='o')
>>>>>>> 1c4491f72963f1a7e0a09f1b407d9107e6f32d4c

plt.show()

<<<<<<< HEAD
##################### Time of Measurements ##############################
# df = pd.DataFrame({'x': excel.df.Date, 'y': excel.df.Time })

# plt.title('Time of measuring')
# plt.plot('x', 'y', data=df, linestyle='none', marker='_')

# # make time human readable from falsedate+time
# xformatter = mdates.DateFormatter('%H:%M')
# plt.gcf().axes[0].yaxis.set_major_formatter(xformatter)

# plt.show()
=======
>>>>>>> 1c4491f72963f1a7e0a09f1b407d9107e6f32d4c
