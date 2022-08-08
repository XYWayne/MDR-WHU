import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import random
from collections import Counter

IN_FILE = '/Users/wangyue/CMPSC/WHU/MDR-WHU/preprocess/raw/Prime_Pantry.csv'

# Get the sorted (by frequency) dataframe from infile, given specified column index want to process
# .rating format: UserID::MovieID::Rating::Timestamp
def get_df(infile, col_index):
	f = open(infile, "r")
	lines = f.readlines()
	col_items = []
	for x in lines:
		col_items.append(str(x.split('\t')[int(col_index)]))
	f.close()

	counter = Counter(col_items)
	data = {'id': list(counter.keys()), 'frequency': list(counter.values())}
	df = pd.DataFrame.from_dict(data)
	df_sorted = df.sort_values(by=['frequency'], ascending=False)
	print(df_sorted.describe())
	return df_sorted

# Get visualization of the dataframe
def draw_distribution(df, save_path=None):
	print(df.describe())
	df['frequency'].plot(title = 'ID Against Frequency', xlabel = 'ID', ylabel = 'Frequency', kind = 'bar', figsize = (12, 8), logy = True)
	plt.xticks([])
	#plt.tight_layout()
	if save_path is not None:
		plt.savefig(save_path)
	else:
		plt.show()

# Process any given input in .csv format into 
def preprocess_raw(infile, outpath):
	df = pd.read_csv(infile, names=['user', 'item', 'rating', 'time'])
	#df.sort_values(by=['user'], ascending=False)
	users = list(df['user'].unique())
	items = list(df['item'].unique())
	users_dict = {}
	items_dict = {}
	# print(users, 'number of unique users: ', len(users))
	# print(items, 'number of unique items: ', len(items))
	for user, i in enumerate(users):
		# print('user: ', type(user), user, ' index: ', type(i), i)
		users_dict[i] = user
	for item, j in enumerate(items):
		items_dict[j] = item
	# print(users_dict)
	# df.replace({"user": users_dict, "item": items_dict},inplace=True)
	df['user'] = df['user'].map(users_dict)
	df['item'] = df['item'].map(items_dict)

	# Filter out the samples that only appear once
	df = df.groupby('user').filter(lambda x: len(x) > 1)
	df = df.sort_values(by=['user'], ascending=True)
	df.to_csv(outpath, sep='\t', header=False, index=False)

# dict_neg records: {user id: {items this user did not rate}}
def get_negative_dict(infile):
	df = pd.read_csv(infile, names=['user', 'item', 'rating', 'time'], sep='\t')
	users = list(df['user'].unique())
	items = list(df['item'].unique())
	dict_neg = {}
	dict_true = {}

	# initialize
	for id in users:
		dict_true[id] = []
		dict_neg[id] = []

	# Fill the true dict up
	f = open(infile, 'r')
	lines = f.readlines()
	for line in lines:
		tokens = line.split('\t')
		user_id = int(tokens[0])
		item_id = int(tokens[1])
		dict_true[user_id].append(item_id)

	# Retrieve 99 random negative samples and insert to true dict if not in it
	for id in users:
		random_list = random.choices(items, k = 99)
		dict_neg[id] = list(set(random_list) - set(dict_true[id]))

	return dict_neg

# Split dataset into train, test, and negative
def split(infile, outpath): # outpath should be a directory
	# Define out file names:
	out_train = f'{outpath}/train.rating'
	out_test = f'{outpath}/test.rating'
	out_negative = f'{outpath}/test.negative'

	f = open(infile, 'r')
	lines = list(f.readlines())
	last_line = lines[-1]
	last_id = last_line.split('\t')[0]
	print(last_id)
	f.close()

	# Creating test set from training set using "leave one out"
	with open(out_train, 'w') as o_tr, open(out_test, 'w') as o_te:
		temp = []
		prev_id = 0
		for line in lines:
			tokens = line.split('\t')
			user_id = int(tokens[0])
			if user_id == prev_id or user_id == last_id:
				temp.append(line)
			else:
				test_line = random.choice(temp)
				temp.remove(test_line)
				o_te.write(test_line)
				for train_line in temp:
					o_tr.write(train_line)
				temp = []
				temp.append(line)
				prev_id = user_id
		# Handling the edge case. Code is ugly though
		test_line = random.choice(temp)
		temp.remove(test_line)
		o_te.write(test_line)
		for train_line in temp:
			o_tr.write(train_line)
	o_tr.close()
	o_te.close()

	# Create negative file form test file
	dict_neg = get_negative_dict(infile)
	f_test = open(out_test, 'r')
	lines_test = f_test.readlines()
	with open(out_negative, 'w') as out_neg:
		for line in lines_test:
			tokens = line.split('\t')
			user_id = int(tokens[0])
			item_id = int(tokens[1])
			neg_list = dict_neg[user_id]
			new_line = f'({user_id},{item_id})'
			for i in range(len(neg_list)):
				new_line += f' \t{neg_list[i]}'
			new_line += ' \n'
			out_neg.write(new_line)
	out_neg.close()

############################################################################################################
# 1. process the raw csv into standard format--userID::itemID::Rating::timestamp
# preprocess_raw(IN_FILE, '/Users/wangyue/CMPSC/WHU/MDR-WHU/preprocess/processed/Prime_Pantry_processed.txt')

# 2. Get the dataframe from the preprocessed files
# df = get_df(sys.argv[1], sys.argv[2])
df = get_df('/Users/wangyue/CMPSC/WHU/MDR-WHU/preprocess/processed/Prime_Pantry_processed.txt', 0)

# 3. Draw the distribution of userID frequency
# draw_distribution(df)

# 4. Split the dataset into train, test, and negative sets
split('/Users/wangyue/CMPSC/WHU/MDR-WHU/preprocess/processed/Prime_Pantry_processed.txt', '.')
# get_negative_dict('/Users/wangyue/CMPSC/WHU/preprocess/processed/Prime_Pantry_processed.txt')