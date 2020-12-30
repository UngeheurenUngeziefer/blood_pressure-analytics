import numpy as np
import pandas as pd
from datetime import date
import pygal


class Pressure:
	''' class aggregating analytics of blood pressure '''

	def __init__(self, excel, sheet_name):
		# open given excel table
		self.df = pd.read_excel(excel, sheet_name)
		#converting to correct datatypes

	def print_df(self):
		# print table
		print(self.df)

	def null_time_value_filling(self):

		
	def converting(self):
		# convert cells of excel to understandable datatypes
		self.df.Date = pd.to_datetime(self.df.Date,
		 									format='%d.%m.%Y')
		self.df.Time = pd.to_datetime(self.df.Time, 
											format='%H:%M:%S').dt.time
		
		self.df.Upper = self.df.Upper.astype(int)
		# self.df.DateTime = str(self.df.Date) + ' ' + str(self.df.Time)


		print(self.df.dtypes)		
		print(self.df)

	

# to show info give filename and sheet name
# excel file need to have columns in order:
# Date, Time, Upper, Down, Pulse, Comments (optional)
obj = Pressure('Pressure.xlsx', 'Pressure')
obj.converting()

