import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import random
from collections import Counter

# Get the sorted (by frequency) dataframe from infile, given specified column index want to process
# .rating format: UserID::MovieID::Rating::Timestamp
def get_df(infile, col_index):
	f = open(infile, "r")
	lines = f.readlines()
	col_items = []
	for x in lines:
		col_items.append(int(x.split('\t')[col_index]))
	f.close()

	counter = Counter(col_items)
	data = {'id': list(counter.keys()), 'frequency': list(counter.values())}
	df = pd.DataFrame.from_dict(data)
	df_sorted = df.sort_values(by=['frequency'], ascending=False)
	return df_sorted

# Get visualization of the dataframe
def draw_distribution(df, save_path=None):
	print(df.describe())
	df['frequency'].plot(title = 'ID Against Frequency', xlabel = 'ID', ylabel = 'Frequency', kind = 'bar', figsize = (12, 8))
	plt.xticks([])
	plt.tight_layout()
	if save_path is not None:
		plt.savefig(save_path)
	else:
		plt.show()

# Split file using given quantile threshold
def split_dataset(dataset, quantile):
	in_file_test = 'Data/' + str(dataset) + '.test.rating'
	out_file_hot_test = 'Data/' + str(dataset) + '.test.hot.rating'
	out_file_lt_test = 'Data/' + str(dataset) + '.test.lt.rating'
	in_file_train = 'Data/' + str(dataset) + '.train.rating'
	out_file_hot_train = 'Data/' + str(dataset) + '.train.hot.rating'
	out_file_lt_train = 'Data/' + str(dataset) + '.train.lt.rating'
	in_file_negative = 'Data/' + str(dataset) + '.test.negative'
	out_file_hot_negative = 'Data/' + str(dataset) + '.test.hot.negative'
	out_file_lt_negative = 'Data/' + str(dataset) + '.test.lt.negative'
	df = get_df(in_file_train, 0)
	with open(in_file_test, 'r') as in_test, open(in_file_train) as in_train, open(in_file_negative) as in_neg:
		threshold = df.quantile(quantile)[1]
		with open(out_file_hot_test, 'w') as out_hot_test, open(out_file_lt_test, 'w') as out_lt_test, open(out_file_hot_train, 'w') as out_hot_train, open(out_file_lt_train, 'w') as out_lt_train, open(out_file_hot_negative, 'w') as out_hot_neg, open(out_file_lt_negative, 'w') as out_lt_neg:
			lines_train = in_train.readlines()
			lines_test = in_test.readlines()
			lines_neg = in_neg.readlines()
			for line_train in lines_train:
				id_train = int(line_train.split('\t')[0])
				frequency_train = df.loc[df['id'] == id_train, 'frequency'].iloc[0]
				print(f'train id:{id_train}, frequency: {frequency_train}, thres: {threshold}')
				if frequency_train >= threshold:
					out_hot_train.write(line_train)
				else:
					out_lt_train.write(line_train)
			for line_test in lines_test:
				id_test = int(line_test.split('\t')[0])
				frequency_test = df.loc[df['id'] == id_test, 'frequency'].iloc[0]
				print(f'test id:{id_test}, frequency: {frequency_test}, thres: {threshold}')
				if frequency_test >= threshold:
					out_hot_test.write(line_test)
				else:
					out_lt_test.write(line_test)
			for line_neg in lines_neg:
				id_neg = int(line_neg.split('\t')[0].split(',')[0].replace('(', ''))
				frequency_neg = df.loc[df['id'] == id_neg, 'frequency'].iloc[0]
				print(f'neg id:{id_neg}, frequency: {frequency_neg}, thres: {threshold}')
				if frequency_neg >= threshold:
					out_hot_neg.write(line_neg)
				else:
					out_lt_neg.write(line_neg)
		out_hot_test.close()
		out_lt_test.close()
		out_hot_train.close()
		out_lt_train.close()
		out_hot_neg.close()
		out_lt_neg.close()
	in_test.close()
	in_train.close()
	in_neg.close()

# Split dataset and manually decrease the number of testing samples by randomly selecting n samples from training data
def split_lt_random(dataset, quantile, n=5):
	in_file_train = 'Data/' + str(dataset) + '.train.rating'
	out_file_hot_train = 'Data/' + str(dataset) + f'.train.hot.rand{n}.rating'
	out_file_lt_train = 'Data/' + str(dataset) + f'.train.lt.rand{n}rating'
	df = get_df(in_file_train, 0)
	with open(in_file_train) as in_train:
		threshold = df.quantile(quantile)[1]
		with open(out_file_hot_train, 'w') as out_hot_train, open(out_file_lt_train, 'w') as out_lt_train:
			lines_train = in_train.readlines()
			temp = [] # Temp buffer to hold all longtail data
			for line_train in lines_train:
				id_train = int(line_train.split('\t')[0])
				frequency_train = df.loc[df['id'] == id_train, 'frequency'].iloc[0]
				print(f'train id:{id_train}, frequency: {frequency_train}, thres: {threshold}')
				if frequency_train >= threshold:
					out_hot_train.write(line_train)
				else:
					temp.append(line_train)
			values = set(map(lambda x:int(x.split('\t')[0]), temp))
			newlist = [[y for y in temp if int(y.split('\t')[0])==x] for x in values]
			# Here we perform the randomization
			for list in newlist:
				for item in random.sample(list, n):
					out_lt_train.write(item)
				

split_lt_random('ml-1m', 0.75)
# def split_dataset(in_file_test, out_file_hot_test, out_file_lt_test, in_file_train, out_file_hot_train, out_file_lt_train, df, quantile):
# df = get_df(IN_FILE_PP_TRAIN, 0)
# draw_distribution(df)
# split_dataset(IN_FILE_PP_TEST, OUT_FILE_PP_TEST_HOT, OUT_FILE_PP_TEST_LT, IN_FILE_PP_TRAIN, OUT_FILE_PP_TRAIN_HOT, OUT_FILE_PP_TRAIN_LT, IN_FILE_PP_NEG, OUT_FILE_PP_NEG_HOT, OUT_FILE_PP_NEG_LT, df, 0.75)