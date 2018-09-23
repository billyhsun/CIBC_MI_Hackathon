import csv
import numpy as np
import pandas as pnd


def open_file(file_name):
	file = pnd.read_csv(file_name, header=None, names = ['FamID', 'FamMemID', 'ProvID', 'ProvType', 'State', 'Date', 'ProcID', 'Cost'])
	#file['State'] = file['State'].apply(state_to_num)
	return file
	