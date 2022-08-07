import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import Counter

IN_FILE_ML_TRAIN = '/Users/wangyue/CMPSC/WHU/MDR/Data/ml-1m.train.rating'
OUT_FILE_ML_TRAIN_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/ml-1m.train.hot.rating'
OUT_FILE_ML_TRAIN_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/ml-1m.train.lt.rating'

IN_FILE_ML_TEST = '/Users/wangyue/CMPSC/WHU/MDR/Data/ml-1m.test.rating'
OUT_FILE_ML_TEST_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/ml-1m.test.hot.rating'
OUT_FILE_ML_TEST_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/ml-1m.test.lt.rating'

IN_FILE_ML_NEG = '/Users/wangyue/CMPSC/WHU/MDR/Data/ml-1m.test.negative'
OUT_FILE_ML_NEG_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/ml-1m.test.hot.negative'
OUT_FILE_ML_NEG_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/ml-1m.test.lt.negative'

#############################################################################################################################

IN_FILE_PI_TRAIN = '/Users/wangyue/CMPSC/WHU/MDR/Data/pinterest-20.train.rating'
OUT_FILE_PI_TRAIN_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/pinterest-20.train.hot.rating'
OUT_FILE_PI_TRAIN_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/pinterest-20.train.lt.rating'

IN_FILE_PI_TEST = '/Users/wangyue/CMPSC/WHU/MDR/Data/pinterest-20.test.rating'
OUT_FILE_PI_TEST_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/pinterest-20.test.hot.rating'
OUT_FILE_PI_TEST_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/pinterest-20.test.lt.rating'

IN_FILE_PI_NEG = '/Users/wangyue/CMPSC/WHU/MDR/Data/pinterest-20.test.negative'
OUT_FILE_PI_NEG_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/pinterest-20.test.hot.negative'
OUT_FILE_PI_NEG_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/pinterest-20.test.lt.negative'

#############################################################################################################################

IN_FILE_YELP_TRAIN = '/Users/wangyue/CMPSC/WHU/MDR/Data/yelp.train.rating'
OUT_FILE_YELP_TRAIN_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/yelp.train.hot.rating'
OUT_FILE_YELP_TRAIN_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/yelp.train.lt.rating'

IN_FILE_YELP_TEST = '/Users/wangyue/CMPSC/WHU/MDR/Data/yelp.test.rating'
OUT_FILE_YELP_TEST_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/yelp.test.hot.rating'
OUT_FILE_YELP_TEST_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/yelp.test.lt.rating'

IN_FILE_YELP_NEG = '/Users/wangyue/CMPSC/WHU/MDR/Data/yelp.test.negative'
OUT_FILE_YELP_NEG_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/yelp.test.hot.negative'
OUT_FILE_YELP_NEG_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/yelp.test.lt.negative'

#############################################################################################################################
IN_FILE_PP_TRAIN = '/Users/wangyue/CMPSC/WHU/MDR/Data/amazon_PP.train.rating'
OUT_FILE_PP_TRAIN_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/amazon_PP.train.hot.rating'
OUT_FILE_PP_TRAIN_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/amazon_PP.train.lt.rating'

IN_FILE_PP_TEST = '/Users/wangyue/CMPSC/WHU/MDR/Data/amazon_PP.test.rating'
OUT_FILE_PP_TEST_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/amazon_PP.test.hot.rating'
OUT_FILE_PP_TEST_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/amazon_PP.test.lt.rating'

IN_FILE_PP_NEG = '/Users/wangyue/CMPSC/WHU/MDR/Data/amazon_PP.test.negative'
OUT_FILE_PP_NEG_HOT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/amazon_PP.test.hot.negative'
OUT_FILE_PP_NEG_LT = '/Users/wangyue/CMPSC/WHU/MDR/Hot_longtail/processed/amazon_PP.test.lt.negative'

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
def split_dataset(in_file_test, out_file_hot_test, out_file_lt_test, in_file_train, out_file_hot_train, out_file_lt_train, in_file_negative, out_file_hot_negative, out_file_lt_negative, df, quantile):
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

# def split_dataset(in_file_test, out_file_hot_test, out_file_lt_test, in_file_train, out_file_hot_train, out_file_lt_train, df, quantile):
df = get_df(IN_FILE_PP_TRAIN, 0)
# draw_distribution(df)
split_dataset(IN_FILE_PP_TEST, OUT_FILE_PP_TEST_HOT, OUT_FILE_PP_TEST_LT, IN_FILE_PP_TRAIN, OUT_FILE_PP_TRAIN_HOT, OUT_FILE_PP_TRAIN_LT, IN_FILE_PP_NEG, OUT_FILE_PP_NEG_HOT, OUT_FILE_PP_NEG_LT, df, 0.75)