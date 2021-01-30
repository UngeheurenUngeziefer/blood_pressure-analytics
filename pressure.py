<<<<<<< HEAD
import numpy as np
import pandas as pd
from datetime import date, timedelta, datetime
import pygal
pd.options.mode.chained_assignment = None


class Pressure:
	''' class aggregating analytics of blood pressure '''

	def __init__(self, excel, sheet_name):
		''' initializing class, open excel, convert datatypes,
			filling empty time records '''

		# open given excel table
		self.df = pd.read_excel(excel, sheet_name)

		# creating datetime column
		self.df['Date'] = self.df['Date'].astype(str)
		self.df['Time'] = self.df['Time'].astype(str)

		for i in range(len(self.df['Date'])):
			if pd.notna(self.df['Time'][i]) == True:
				self.df['DateTime'][i] = self.df.Date + " " + self.df.Time
			elif pd.notna(self.df['Time'][i]) == False:
				self.df['DateTime'][i] = self.df['Date']
		self.df['DateTime'] = pd.to_datetime(self.df['DateTime'], format='%Y.%m.%d %H:%M:%S')

		# converting to correct datatypes
		self.df.Date = pd.to_datetime(self.df.Date,	format='%d.%m.%Y')
		self.df.Time = pd.to_datetime(self.df.Time, format='%H:%M:%S').dt.time
		
		# creating frequency of measurements column
		self.df['Date_freq'] = \
							self.df.groupby('Date')['Date'].transform('count')

		self.df['Sum of systolic and diastolic pressure'] = self.df.Upper + self.df.Down

		# filling the empty time records if we know time of near records
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


		print(self.df.dtypes)


	def minus_2_hours(self, index):
		'''function extract 2 hours from previous time and return timestamp'''
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


	def new_dates_columns(self):
		'''creating columns related to dates'''
		self.df['Measurements_per_month'] = \
			self.df.Date.groupby(
			[self.df.Date.dt.year, self.df.Date.dt.month]).transform('count')
		
		self.df['Measurements_per_year'] = \
			self.df.Date.groupby(
			[self.df.Date.dt.year]).transform('count')

		list_of_unique_series = self.df.Date.unique()
		self.df['Unique_dates'] = \
			pd.DataFrame(list_of_unique_series)
		pd.to_datetime(self.df.Unique_dates, format='%d.%m.%Y')

		self.df['Days_of_observations_per_month'] = \
			self.df.Unique_dates.groupby(
				[self.df.Unique_dates.dt.year, 
				 self.df.Unique_dates.dt.month]).transform('count')

		self.df['Days_of_observations_per_years'] = \
			self.df.Unique_dates.groupby(
				[self.df.Unique_dates.dt.year]).transform('count')


	def new_times_columns(self):
		'''creating columns related to time'''
		self.df['Times_of_day_4'] = self.df['Time']
		self.df['Times_of_day_2'] = self.df['Time']
		self.df['Season'] = self.df['Date']

		# creating time 2 types
		for i in range(len(self.df['Times_of_day_2'])):
			if self.df['Times_of_day_2'].iloc[i] >= datetime.strptime('5:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_2'].iloc[i] < datetime.strptime('17:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_2'].iloc[i] = 'Day'
			elif self.df['Times_of_day_2'].iloc[i] >= datetime.strptime('17:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_4'].iloc[i] <= datetime.strptime('23:59:59', '%H:%M:%S').time() \
			or self.df['Times_of_day_2'].iloc[i] < datetime.strptime('5:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_2'].iloc[i] = 'Night'
			else:
				self.df.Time.iloc[i] = ''

		# creating time 4 types
		for i in range(len(self.df['Times_of_day_4'])):
			if self.df['Times_of_day_4'].iloc[i] >= datetime.strptime('5:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_4'].iloc[i] < datetime.strptime('11:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_4'].iloc[i] = 'Morning'
			elif self.df['Times_of_day_4'].iloc[i] >= datetime.strptime('11:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_4'].iloc[i] < datetime.strptime('17:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_4'].iloc[i] = 'Day'
			elif self.df['Times_of_day_4'].iloc[i] >= datetime.strptime('17:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_4'].iloc[i] < datetime.strptime('23:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_4'].iloc[i] = 'Evening'
			elif self.df['Times_of_day_4'].iloc[i] >= datetime.strptime('23:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_4'].iloc[i] <= datetime.strptime('23:59:59', '%H:%M:%S').time() \
			or self.df['Times_of_day_4'].iloc[i] < datetime.strptime('5:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_4'].iloc[i] = 'Night'
			else:
				self.df['Times_of_day_4'].iloc[i] = ''

		# creating season column
		for i in range(len(self.df['Season'])):
			if self.df['Season'].iloc[i].month in (12, 1, 2):
				self.df['Season'].iloc[i] = 'Winter'
			elif self.df['Season'].iloc[i].month in (3, 4, 5):
				self.df['Season'].iloc[i] = 'Spring'
			elif self.df['Season'].iloc[i].month in (6, 7, 8):
				self.df['Season'].iloc[i] = 'Summer'
			elif self.df['Season'].iloc[i].month in (9, 10, 11):
				self.df['Season'].iloc[i] = 'Autumn'
			else:
				self.df['Season'].iloc[i] = ''


	def print_info(self):
		''' print basic info '''
		
		average_measurements = sum(self.df.Date_freq) / len(self.df.Date_freq)
		maximum_measurements = max(self.df.Date_freq)
		minimum_measurements = min(self.df.Date_freq)
		total_measurements	 = len(self.df.Date)
		
		self.df.at[0, 'Avg number of measurements per day'] = str(average_measurements)[0:4]
		self.df.at[0, 'Min number of measurements per day'] = str(minimum_measurements)
		self.df.at[0, 'Max number of measurements per day'] = str(maximum_measurements)
		self.df.at[0, 'Total number of measuremets'] = str(total_measurements)
		self.df.at[0, 'Avg number of systolic pressure'] = self.df.Upper.mean()
		self.df.at[0, 'Min number of systolic pressure'] = min(self.df.Upper)
		self.df.at[0, 'Max number of systolic pressure'] = max(self.df.Upper)
		self.df.at[0, 'Avg number of diastolic pressure'] = self.df.Down.mean()
		self.df.at[0, 'Min number of diastolic pressure'] = min(self.df.Down)
		self.df.at[0, 'Max number of diastolic pressure'] = max(self.df.Down)
		self.df.at[0, 'Avg number of pulse'] = self.df.Pulse.mean()
		self.df.at[0, 'Min number of pulse'] = min(self.df.Pulse)
		self.df.at[0, 'Max number of pulse'] = max(self.df.Pulse)
		self.df.at[0, 'Max of sum of systolic and diastolic pressure'] = max(self.df['Sum of systolic and diastolic pressure'])
		self.df.at[0, 'Min of sum of systolic and diastolic pressure'] = min(self.df['Sum of systolic and diastolic pressure'])
		


		print('Total measurements per year: ')
		print(self.df.groupby([self.df.Date.dt.year]
							 )['Measurements_per_year'].count().to_string())

		print('Total measurements per month: ')
		print(self.df.groupby([self.df.Date.dt.year,
			 				   self.df.Date.dt.month]
							 )['Measurements_per_month'].count().to_string())
		print('Total measurements per day: ')
		print(self.df.groupby([self.df.Date.dt.year,
						 	   self.df.Date.dt.month, 
						 	   self.df.Date.dt.day]
							 )['Date_freq'].count().to_string())
		print('Days of measurements per year: ')
		print(self.df.groupby([self.df.Unique_dates.dt.year.map('{:.0f}'.format)]
						 	 )['Unique_dates'].count().to_string())
		print('Days of measurements per month: ')
		print(self.df.groupby([self.df.Unique_dates.dt.year.map('{:.0f}'.format),
						 	   self.df.Unique_dates.dt.month.map('{:.0f}'.format)]
						 	 )['Unique_dates'].count().to_string())
		print('Times of day of measurements format-4: ')
		print(self.df.groupby(self.df.Times_of_day_4)['Date'].count().to_string())
		print('Times of day of measurements format-2: ')
		print(self.df.groupby(self.df.Times_of_day_2)['Date'].count().to_string())
		print('Season of measurements: ')
		print(self.df.groupby(self.df.Season)['Date'].count().rename({'Season':'asd'}).to_string())



#excel.print_df()
excel = Pressure('res/Pressure.xlsx', 'Pressure')
excel.new_dates_columns()
excel.new_times_columns()

# excel.print_info()

# excel.save_df('C:/Users/sewer/MyPython/Blood Pressure Analytics/res/Output Table.csv')

=======
import numpy as np
import pandas as pd
from datetime import date, timedelta, datetime
import pygal
pd.options.mode.chained_assignment = None


class Pressure:
	''' class aggregating analytics of blood pressure '''

	def __init__(self, excel, sheet_name):
		''' initializing class, open excel, convert datatypes,
			filling empty time records '''

		# open given excel table
		self.df = pd.read_excel(excel, sheet_name)

		# converting to correct datatypes
		self.df.Date = pd.to_datetime(self.df.Date,	format='%d.%m.%Y')
		self.df.Time = pd.to_datetime(self.df.Time, format='%H:%M:%S').dt.time
		
		# creating frequency of measurements column
		self.df['Date_freq'] = \
							self.df.groupby('Date')['Date'].transform('count')

		self.df['Sum of systolic and diastolic pressure'] = self.df.Upper + self.df.Down

		# filling the empty time records if we know time of near records
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
		'''function extract 2 hours from previous time and return timestamp'''
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


	def new_dates_columns(self):
		'''creating columns related to dates'''
		self.df['Measurements_per_month'] = \
			self.df.Date.groupby(
			[self.df.Date.dt.year, self.df.Date.dt.month]).transform('count')
		
		self.df['Measurements_per_year'] = \
			self.df.Date.groupby(
			[self.df.Date.dt.year]).transform('count')

		list_of_unique_series = self.df.Date.unique()
		self.df['Unique_dates'] = \
			pd.DataFrame(list_of_unique_series)
		pd.to_datetime(self.df.Unique_dates, format='%d.%m.%Y')

		self.df['Days_of_observations_per_month'] = \
			self.df.Unique_dates.groupby(
				[self.df.Unique_dates.dt.year, 
				 self.df.Unique_dates.dt.month]).transform('count')

		self.df['Days_of_observations_per_years'] = \
			self.df.Unique_dates.groupby(
				[self.df.Unique_dates.dt.year]).transform('count')


	def new_times_columns(self):
		'''creating columns related to time'''
		self.df['Times_of_day_4'] = self.df['Time']
		self.df['Times_of_day_2'] = self.df['Time']
		self.df['Season'] = self.df['Date']

		# creating time 2 types
		for i in range(len(self.df['Times_of_day_2'])):
			if self.df['Times_of_day_2'].iloc[i] >= datetime.strptime('5:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_2'].iloc[i] < datetime.strptime('17:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_2'].iloc[i] = 'Day'
			elif self.df['Times_of_day_2'].iloc[i] >= datetime.strptime('17:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_4'].iloc[i] <= datetime.strptime('23:59:59', '%H:%M:%S').time() \
			or self.df['Times_of_day_2'].iloc[i] < datetime.strptime('5:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_2'].iloc[i] = 'Night'
			else:
				self.df.Time.iloc[i] = ''

		# creating time 4 types
		for i in range(len(self.df['Times_of_day_4'])):
			if self.df['Times_of_day_4'].iloc[i] >= datetime.strptime('5:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_4'].iloc[i] < datetime.strptime('11:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_4'].iloc[i] = 'Morning'
			elif self.df['Times_of_day_4'].iloc[i] >= datetime.strptime('11:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_4'].iloc[i] < datetime.strptime('17:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_4'].iloc[i] = 'Day'
			elif self.df['Times_of_day_4'].iloc[i] >= datetime.strptime('17:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_4'].iloc[i] < datetime.strptime('23:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_4'].iloc[i] = 'Evening'
			elif self.df['Times_of_day_4'].iloc[i] >= datetime.strptime('23:00:00', '%H:%M:%S').time() \
			and self.df['Times_of_day_4'].iloc[i] <= datetime.strptime('23:59:59', '%H:%M:%S').time() \
			or self.df['Times_of_day_4'].iloc[i] < datetime.strptime('5:00:00', '%H:%M:%S').time():
				self.df['Times_of_day_4'].iloc[i] = 'Night'
			else:
				self.df['Times_of_day_4'].iloc[i] = ''

		# creating season column
		for i in range(len(self.df['Season'])):
			if self.df['Season'].iloc[i].month in (12, 1, 2):
				self.df['Season'].iloc[i] = 'Winter'
			elif self.df['Season'].iloc[i].month in (3, 4, 5):
				self.df['Season'].iloc[i] = 'Spring'
			elif self.df['Season'].iloc[i].month in (6, 7, 8):
				self.df['Season'].iloc[i] = 'Summer'
			elif self.df['Season'].iloc[i].month in (9, 10, 11):
				self.df['Season'].iloc[i] = 'Autumn'
			else:
				self.df['Season'].iloc[i] = ''


	def print_info(self):
		''' print basic info '''
		
		average_measurements = sum(self.df.Date_freq) / len(self.df.Date_freq)
		maximum_measurements = max(self.df.Date_freq)
		minimum_measurements = min(self.df.Date_freq)
		total_measurements	 = len(self.df.Date)
		
		self.df.at[0, 'Avg number of measurements per day'] = str(average_measurements)[0:4]
		self.df.at[0, 'Min number of measurements per day'] = str(minimum_measurements)
		self.df.at[0, 'Max number of measurements per day'] = str(maximum_measurements)
		self.df.at[0, 'Total number of measuremets'] = str(total_measurements)
		self.df.at[0, 'Avg number of systolic pressure'] = self.df.Upper.mean()
		self.df.at[0, 'Min number of systolic pressure'] = min(self.df.Upper)
		self.df.at[0, 'Max number of systolic pressure'] = max(self.df.Upper)
		self.df.at[0, 'Avg number of diastolic pressure'] = self.df.Down.mean()
		self.df.at[0, 'Min number of diastolic pressure'] = min(self.df.Down)
		self.df.at[0, 'Max number of diastolic pressure'] = max(self.df.Down)
		self.df.at[0, 'Avg number of pulse'] = self.df.Pulse.mean()
		self.df.at[0, 'Min number of pulse'] = min(self.df.Pulse)
		self.df.at[0, 'Max number of pulse'] = max(self.df.Pulse)
		self.df.at[0, 'Max of sum of systolic and diastolic pressure'] = max(self.df['Sum of systolic and diastolic pressure'])
		self.df.at[0, 'Min of sum of systolic and diastolic pressure'] = min(self.df['Sum of systolic and diastolic pressure'])
		


		# print('Total measurements per year: ')
		# print(self.df.groupby([self.df.Date.dt.year]
		# 					 )['Measurements_per_year'].count().to_string())

		# print('Total measurements per month: ')
		# print(self.df.groupby([self.df.Date.dt.year,
		# 	 				   self.df.Date.dt.month]
		# 					 )['Measurements_per_month'].count().to_string())
		# print('Total measurements per day: ')
		# print(self.df.groupby([self.df.Date.dt.year,
		# 				 	   self.df.Date.dt.month, 
		# 				 	   self.df.Date.dt.day]
		# 					 )['Date_freq'].count().to_string())
		# print('Days of measurements per year: ')
		# print(self.df.groupby([self.df.Unique_dates.dt.year.map('{:.0f}'.format)]
		# 				 	 )['Unique_dates'].count().to_string())
		# print('Days of measurements per month: ')
		# print(self.df.groupby([self.df.Unique_dates.dt.year.map('{:.0f}'.format),
		# 				 	   self.df.Unique_dates.dt.month.map('{:.0f}'.format)]
		# 				 	 )['Unique_dates'].count().to_string())
		# print('Times of day of measurements format-4: ')
		# print(self.df.groupby(self.df.Times_of_day_4)['Date'].count().to_string())
		# print('Times of day of measurements format-2: ')
		# print(self.df.groupby(self.df.Times_of_day_2)['Date'].count().to_string())
		# print('Season of measurements: ')
		# print(self.df.groupby(self.df.Season)['Date'].count().rename({'Season':'asd'}).to_string())



#excel.print_df()
excel = Pressure('res/Pressure.xlsx', 'Pressure')

excel.new_dates_columns()
excel.new_times_columns()
excel.print_info()
# excel.save_df('C:/Users/sewer/MyPython/Blood Pressure Analytics/Output Table.csv')

>>>>>>> db1ef6af8a1f7fe894a1d6b8d513ee7ffcbb8d08
