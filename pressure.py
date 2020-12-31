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
		#converting to correct datatypes
		self.df.Date = pd.to_datetime(self.df.Date,
		 									format='%d.%m.%Y')
		self.df.Time = pd.to_datetime(self.df.Time, 
											format='%H:%M:%S').dt.time
		# average time of measurements
		self.df['Date_freq'] = self.df.groupby('Date')['Date'].transform('count')

		# for every index of column
		for i in range(len(self.df.Time)):
			# if Time is Null and previous not Null
			# if Date is same and there 4 or less dates
			if pd.isnull(self.df.Time[i]) == True \
			   and pd.isnull(self.df.Time[i - 1]) == False \
			   and self.df.Date[i] == self.df.Date[i - 1] \
			   and self.df.Date_freq[i] <= 4:
				self.df.Time[i] = self.df.Time[i - 1]
			else:
				print('full')
		

	def print_df(self):
		# print table
		# print(self.df.head(50))
		print(self.df.Date_freq.unique())

		
	def converting(self):
		# convert cells of excel to understandable datatypes
		
		
		self.df.Upper = self.df.Upper.astype(int)
		# self.df.DateTime = str(self.df.Date) + ' ' + str(self.df.Time)


		print(self.df.dtypes)		
		print(self.df)

	

# to show info give filename and sheet name
# excel file need to have columns in order:
# Date, Time, Upper, Down, Pulse, Comments (optional)
obj = Pressure('Pressure.xlsx', 'Pressure')
obj.print_df()

