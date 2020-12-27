import numpy as np
import pandas as pd
from datetime import date
import pygal

# pressure table
pressure = pd.read_excel('Pressure.xlsx', sheet_name='Pressure')

# convert into datetime
pressure['Date'] = pd.to_datetime(pressure['Date'],	format='%d.%M.%Y')
# print(pressure.dtypes)

# show datatypes and table
# print(pressure.dtypes)
# print(pressure)

first_date = pressure['Date'].iloc[0]
last_date  = pressure['Date'].iloc[len(pressure) - 1]
period = last_date - first_date
# print(period)

days_measured = len(pressure.groupby(['Date']).mean())

# pygal chart
# line_chart = pygal.StackedBar()
# line_chart.title = 'title'
# line_chart.add('name', [69.47])
# line_chart.add('name', [30.53])
# line_chart.render()
# line_chart.render_to_file('chart.svg')

records_per_day = 0

pressure['rec_per_day'] = pressure.groupby('Date')['Date'].transform('count')
mean_measures_per_day = pressure['rec_per_day'].mean()
# print(mean_measures_per_day)

print(pressure.groupby(pressure['Date'].dt.strftime('%M'))['rec_per_day'].sum().sort_values())
