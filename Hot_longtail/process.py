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

# Same as the above, but we want all the samples comming from the lt part.
def split_lt_random_hot(dataset, quantile, n=5, sample = False):
	in_file_train = 'Data/' + str(dataset) + '.train.rating'
	out_file_hot_train = 'Data/' + str(dataset) + f'.train.hot.hotitem.rating'
	out_file_lt_train = 'Data/' + str(dataset) + f'.train.lt.hotitem.rating'
	df = get_df(in_file_train, 0)
	df_item = get_df(in_file_train, 1) # get the item df
	with open(in_file_train) as in_train:
		threshold = df.quantile(quantile)[1]
		threshold_item = df_item.quantile(quantile)[1]
		with open(out_file_hot_train, 'w') as out_hot_train, open(out_file_lt_train, 'w') as out_lt_train:
			lines_train = in_train.readlines()
			temp = [] # Temp buffer to hold all longtail data
			for line_train in lines_train:
				id_train = int(line_train.split('\t')[0])
				id_train_item = int(line_train.split('\t')[1])
				frequency_train = df.loc[df['id'] == id_train, 'frequency'].iloc[0]
				frequency_item = df_item.loc[df_item['id'] == id_train_item, 'frequency'].iloc[0]
				print(f'train id:{id_train}, frequency: {frequency_train}, thres: {threshold}')
				if frequency_train >= threshold:
					out_hot_train.write(line_train)
				elif frequency_item < threshold_item:
					if sample == True:
						temp.append(line_train)
					else:
						out_lt_train.write(line_train)
			if sample == True:
				values = set(map(lambda x:int(x.split('\t')[0]), temp))
				newlist = [[y for y in temp if int(y.split('\t')[0])==x] for x in values]
				# Here we perform the randomization
				for list in newlist:
					for item in random.sample(list, n):
						out_lt_train.write(item)
				
# Given a dataset, report the number of items from hot and longtail part.
def analyze_component(dataset, filename, quantile):
	in_train = 'Data/' + str(dataset) + '.train.rating'
	user_df = get_df(in_train, 0) # col_index = 0 --> userID
	item_df = get_df(in_train, 1) # col_index = 1 --> itemID
	user_threshold = user_df.quantile(quantile)[1]
	item_threshold = item_df.quantile(quantile)[1]
	hot_item_count, lt_item_count = 0, 0
	hot_user_count, lt_user_count = 0, 0
	num_user_id = len(user_df)
	num_item_id = len(item_df)
	with open(filename, 'r') as infile:
		lines = infile.readlines()
		for line in lines:
			user_id = int(line.split('\t')[0])
			item_id = int(line.split('\t')[1])
			if (user_df['id'].eq(user_id)).any(): # Check if the user is in the random sample
				frequency = user_df.loc[user_df['id'] == user_id, 'frequency'].iloc[0]
				if frequency >= user_threshold:
					hot_user_count += 1
				else:
					lt_user_count += 1
			if (item_df['id'].eq(item_id)).any(): # Check if the user is in the random sample
				frequency = item_df.loc[item_df['id'] == item_id, 'frequency'].iloc[0]
				if frequency >= item_threshold:
					hot_item_count += 1
				else:
					lt_item_count += 1
	# Report user stats: number of userID, number of hot&lt users
	print(f'Number of hot users: {hot_user_count}, number of lt users: {lt_user_count}')
	print(f'Number of hot items: {hot_item_count}, number of lt items: {lt_item_count}\n')

# for perc in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
# 	dataset = 'ml-1m'
# 	file = f'Data/{dataset}.train.hot{perc}%lt.rating'
# 	# file = f'Hot_longtail/lesser_samples/{dataset}.train.hot{perc}%lt.rand5.rating'
# 	analyze_component(dataset, file, 0.75)

split_lt_random_hot('yelp', 0.75, sample=False)
# split_lt_random('yelp', 0.75)
# df = get_df(IN_FILE_PP_TRAIN, 0)
# draw_distribution(df)
# analyze_component('yelp', 'Data/yelp.train.lt.rand5rating', 0.75)