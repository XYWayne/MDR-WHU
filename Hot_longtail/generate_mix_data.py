import random

INPATH = 'Data/'
OUTPATH = 'Hot_longtail/mixed_data/'

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_mix_data(dataset):
	random.seed(42)
	# paths to hot files
	in_file_train_hot = INPATH + str(dataset) + '.train.hot.rating'
	in_file_test_hot = INPATH + str(dataset) + '.test.hot.rating'
	in_file_hot_negative = INPATH + str(dataset) + '.test.hot.negative'
	# paths to longtail files
	in_file_train_lt = INPATH + str(dataset) + '.train.lt.rating'
	in_file_test_lt = INPATH + str(dataset) + '.test.lt.rating'
	in_file_lt_negative = INPATH + str(dataset) + '.test.lt.negative'

	# Read in all datalines and shuffle
	id = []
	in_train = list(open(in_file_train_lt, 'r').readlines())
	random.shuffle(in_train)
	for line in in_train:
		id_line = line.split('\t')[0]
		if id_line not in id:
			id.append(id_line)

	# Split data by id
	id_splited = list(chunks(id, len(id)//10))

	# Merge the last 2 lists if exists
	if len(id_splited) > 10:
		id_splited[9] += id_splited[10]
	# for sublist in id_splited:
	# 	print(len(sublist))

	# Start writing into hot file (10%)
	for perc in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
		print(f'Creating mixed data of hot and {perc}% longtail.')
		num_id_list = perc // 10
		id_list = []
		for i in range(num_id_list):
			id_list += id_splited[i]
		
		corpus_train = []
		print('Creating training data...')
		with open(in_file_train_hot, 'r') as in_train_hot:
			data_hot = in_train_hot.readlines()
			for line in data_hot:
				corpus_train.append(line)
		with open(in_file_train_lt, 'r') as in_train_lt:
			lt_data = in_train_lt.readlines()
			for line in lt_data:
				temp_id = line.split('\t')[0]
				if temp_id in id_list:
					# print(f'id{temp_id} found in longtail split.')
					corpus_train.append(line)
		
		# Sort corpus by id
		corpus_train.sort(key = lambda x: int(x.split('\t')[0]))
		with open(OUTPATH + str(dataset) + f'.train.hot{perc}%lt.rating', 'w') as out_train:
			for line in corpus_train:
				out_train.write(line)
		
		corpus_test = []
		print('Creating test data...')
		with open(in_file_test_hot, 'r') as in_test_hot:
			data_hot = in_test_hot.readlines()
			for line in data_hot:
				corpus_test.append(line)
	
		with open(in_file_test_lt, 'r') as in_test_lt:
			lt_data = in_test_lt.readlines()
			for line in lt_data:
				temp_id = line.split('\t')[0]
				if temp_id in id_list:
					# print(f'id{temp_id} found in longtail split.')
					corpus_test.append(line)
		
		corpus_test.sort(key = lambda x: int(x.split('\t')[0]))
		with open(OUTPATH + str(dataset) + f'.test.hot{perc}%lt.rating', 'w') as out_test:
			for line in corpus_test:
				out_test.write(line)

		corpus_neg = []
		print('Creating negative data...')
		with open(in_file_hot_negative, 'r') as in_neg_hot:
			data_hot = in_neg_hot.readlines()
			for line in data_hot:
				corpus_neg.append(line)
	
		with open(in_file_lt_negative, 'r') as in_neg_lt:
			lt_data = in_neg_lt.readlines()
			for line in lt_data:
				temp_id = line.split('\t')[0].split(',')[0].replace('(', '')
				if temp_id in id_list:
					# print(f'id{temp_id} found in longtail split.')
					corpus_neg.append(line)
		corpus_neg.sort(key = lambda x: int(x.split('\t')[0].split(',')[0].replace('(', '')))
		with open(OUTPATH + str(dataset) + f'.test.hot{perc}%lt.negative', 'w') as out_neg:
			for line in corpus_neg:
				out_neg.write(line)


get_mix_data('yelp')
