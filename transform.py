import os
import tabula as tb
import pandas as pd
import numpy as np
from download import current_year, today
from config import destination_folder, csv_path, starting_year


def read_and_transform_dosar_pdfs(folder_path=destination_folder, 
	starting_year=starting_year, 
	csv_path=csv_path, 
	current_year=current_year, 
	today=today):

	# Set the area to extract pdf (top, left, bottom, right)
	area = [73.5, 22.5, 908, 962]

	# set empty dataframe
	merged_df = pd.DataFrame()

	for file_name in os.listdir(folder_path):
		# Include only files from starting year to today's year
		if any(str(year) in file_name for year in range(starting_year, current_year + 1)):
			print(file_name)
			file_path = os.path.join(folder_path, file_name)

	        # Extract the table from the specified area of the PDF and convert it to a pandas DataFrame
			df = tb.read_pdf(file_path, pages='all', stream=True, guess=False, area=area)

			# merge list of data frames
			mid_df = pd.concat(df, ignore_index=True)

			# merge with empty data frame
			merged_df = pd.concat([merged_df, mid_df], ignore_index=True)

	# change the columns names
	dosar = merged_df.rename(columns={'NR. DOSAR': 'dosar',
	                                  'DATA ÎNREGISTRĂRII': 'registration_date', 
	                                  'TERMEN': 'review_date', 
	                                  'SOLUȚIE': 'solution'})

	# there were obvious mistakes spotted in pdfs, so we check for registration_date
	# to be the same if between the same ones
	for i in range(1, len(dosar) - 1):
		# check if the current date is different from the previous and next values
		if (dosar.iloc[i, 1] != dosar.iloc[i - 1, 1] and 
			dosar.iloc[i, 1] != dosar.iloc[i + 1, 1]):
        		# take the previous date
        		dosar.iloc[i, 1] = dosar.iloc[i - 1, 1]

	# change dates to datetime
	dosar['registration_date'] = pd.to_datetime(dosar['registration_date'], format='%d.%m.%Y')
	dosar['review_date'] = pd.to_datetime(dosar['review_date'], format='%d.%m.%Y')

	# create week, month, and year starts
	dosar['registration_week'] = dosar['registration_date'].dt.to_period('w').dt.start_time
	dosar['registration_month'] = dosar['registration_date'].dt.to_period('M')
	dosar['registration_year'] = dosar['registration_date'].dt.to_period('Y')

	# add reviewing time in days
	dosar['reviewing_days'] = dosar['review_date'] - dosar['registration_date']
	dosar['reviewing_days'] = dosar['reviewing_days'].dt.total_seconds().astype(float) / 86400

	# split solution to get a solution number and date
	dosar['solution_number'] = dosar['solution'].str.split('/', expand=True)[0]
	dosar['solution_date'] = dosar['solution'].str[-10:]

	# add solution time in days
	dosar['solution_date'] = pd.to_datetime(dosar['solution_date'], format='%d.%m.%Y', errors='coerce')
	dosar['solution_days'] = dosar['solution_date'] - dosar['registration_date']
	dosar['solution_days'] = dosar['solution_days'].dt.total_seconds().astype(float) / 86400

	# add a new column 'last_update' and set the first row value to today's date
	dosar.loc[0, 'last_update'] = today

	# Check if csv exists and rename columns in old dosar data frame
	if os.path.isfile(csv_path):
		old_dosar = pd.read_csv(csv_path)
		old_dosar = old_dosar.drop(['old_dosar', 'old_solution'], axis=1)
		old_dosar = old_dosar.rename(columns={'dosar': 'old_dosar', 'solution': 'old_solution'})
	else:
		old_dosar = pd.DataFrame()
		old_dosar.columns = ['old_dosar', 'old_solution']

	# merge with old dosar data frame
	dosar = dosar.merge(old_dosar[['old_dosar', 'old_solution']], how='left', left_on='dosar', right_on='old_dosar')

	# define function for solution flag
	def solution_flag(row):
		if not pd.isna(row['old_solution']):
			return 'yes'
		elif not pd.isna(row['solution']):
			return 'yes (new)'
		else:
			return 'no'

	# add a solution flag column
	dosar['solution_flag'] = dosar.apply(solution_flag, axis=1)

	# Check if the file exists
	if os.path.isfile(csv_path):
		# If the file exists, overwrite it with the new data
		dosar.to_csv(csv_path, mode='w', index=False)
	else:
		# If the file doesn't exist, create a new one
		dosar.to_csv(csv_path, mode='x', index=False)