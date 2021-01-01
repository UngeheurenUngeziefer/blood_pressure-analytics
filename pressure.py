import numpy as np
import pandas as pd
from datetime import date, timedelta, datetime
import pygal
pd.options.mode.chained_assignment = None


class Pressure:
	''' class aggregating analytics of blood pressure '''

	def __init__(self, excel, sheet_name):
		# open given excel table
		self.df = pd.read_excel(excel, sheet_name)

		# converting to correct datatypes
		self.df.Date = pd.to_datetime(self.df.Date,	format='%d.%m.%Y')
		self.df.Time = pd.to_datetime(self.df.Time, format='%H:%M:%S').dt.time
		
		# frequency of measurements
		self.df['Date_freq'] = \
							self.df.groupby('Date')['Date'].transform('count')

		# for every index of column
		for i in range(len(self.df.Time)):
			
			# if Time is Null and previous not Null and Date the same
			if pd.isnull(self.df.Time[i]) == True \
			and pd.isnull(self.df.Time[i - 1]) == False \
			and self.df.Date[i] == self.df.Date[i - 1]:
				self.df.Time[i] = self.df.Time[i - 1]
			
			# if we have time after but dont have at the start
			# if first record is empty
			elif pd.isnull(self.df.Time[i]) == True \
			and self.df.Date[i] != self.df.Date[i - 1]:
				
				# for every record of this date
				for j in range(self.df.Date_freq[i]):
				
					# if every next record is empty
					if pd.isnull(self.df.Time[i + j]) == True:
						pass
				
					# if next record filled
					else:
						# set first empty record equal to next filled - 2h
						if pd.isnull(self.df.Time[i]) == True:
							self.df.Time[i] = self.minus_2_hours(i + j)
						# if it already filled pass
						else:
							pass
			else:
				pass

	def minus_2_hours(self, index):
		'''function extract 2 hours and return timestamp'''
		delta = timedelta(hours = 2)
		current_date = date(self.df.Date[index].year, \
							self.df.Date[index].month, \
							self.df.Date[index].day)

		minused_time = (datetime.combine(current_date, \
					self.df.Time[index]) - delta).time()

		return minused_time


	def save_df(self, address):
		'''save table into csv'''
		self.df.to_csv(address)
		print('Data saved')


	def print_df(self):
		'''print dataframe'''
		print(self.df)


	def measurements_analytics(self):
		average_measurements = sum(self.df.Date_freq) / len(self.df.Date_freq)
		maximum_measurements = max(self.df.Date_freq)
		minimum_measurements = min(self.df.Date_freq)
		sum_measurements	 = sum(self.df.Date_freq)


	def dates_analytics(self):
		self.df['Measurements_per_month'] = \
			self.df.Date.groupby(
			[self.df.Date.dt.year, self.df.Date.dt.month]).transform('count')
		
		self.df['Measurements_per_year'] = \
			self.df.Date.groupby(
			[self.df.Date.dt.year]).transform('count')

		list_of_unique_series = self.df.Date.unique()
		self.df['Unique_dates'] = \
			pd.DataFrame(list_of_unique_series)

		self.df['Days_of_observations_per_month'] = \
			self.df.Unique_dates.groupby(
				[self.df.Unique_dates.dt.year, 
				 self.df.Unique_dates.dt.month]).transform('count')

		self.df['Days_of_observations_per_years'] = \
			self.df.Unique_dates.groupby(
				[self.df.Unique_dates.dt.year]).transform('count')

	def time_analytics(self):
		for i in self.df.Time:
			datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
			if i >= datetime.strptime('5:00:00', '%H:%M:%S').time() \
			and i < datetime.strptime('11:00:00', '%H:%M:%S').time():
				print('Morning')
		# self.df['Times_of_day'] = \
		# same with season


	def print_info(self):
		print('Avg number of measurements is ' + str(average_measurements)[0:4])
		print('Min number of measurements is ' + str(minimum_measurements))
		print('Max number of measurements is ' + str(maximum_measurements))
		print('Total number of measuremets is ' + str(sum_measurements)) 
			

excel = Pressure('res/Pressure.xlsx', 'Pressure')
#excel.print_df()

# excel.measurements_analytics()
# excel.dates_analytics()
# excel.save_df('C:/Users/sewer/MyPython/Blood Pressure Analytics/Output Table.csv')
excel.time_analytics()