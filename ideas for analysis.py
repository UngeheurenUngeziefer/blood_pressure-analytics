# if we have time in evening but dont have at the morning 6 5 3
			elif pd.isnull(self.df.Time[i]) == True \
			   and pd.isnull(self.df.Time[i + 1]) == True \
			   and pd.isnull(self.df.Time[i + 2]) == True \
			   and pd.isnull(self.df.Time[i + 3]) == False \
			   and self.df.Date_freq[i] > 4:
				delta = timedelta(hours = 2)
				current_date = date(self.df.Date[i].year, \
									self.df.Date[i].month, \
									self.df.Date[i].day)

				self.df.Time[i] = (datetime.combine(current_date, self.df.Time[i + 3]) - delta).time()


				
# convert into datetime
pressure['Date'] = pd.to_datetime(pressure['Date'],	format='%d.%M.%Y')
# print(pressure.dtypes)

# show datatypes and table
# print(pressure.dtypes)
# print(pressure)
print(self.df.Date_freq.unique())
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
