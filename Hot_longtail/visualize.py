import matplotlib.pyplot as plt

ml_hr = [0.5436, 0.5801, 0.5940, 0.6086, 0.6248, 0.6415, 0.6520, 0.6612, 0.6793, 0.6816] # 0.6612, 0.6793
ml_ndcg = [0.2978, 0.3204, 0.3310, 0.3477, 0.3517, 0.3708, 0.3788, 0.3889, 0.4021, 0.4053] # 0.3889, 0.4021

ml_hr_rand = [0.5318, 0.5259, 0.5337, 0.5462, 0.5484, 0.5562, 0.5660, 0.5662, 0.5641, 0.5700]
ml_ndcg_rand = [0.2876, 0.2849, 0.2961, 0.2990, 0.3064, 0.3086, 0.3162, 0.3183, 0.3155, 0.3195]

yelp_hr_rand = [0.7159, 0.7173, 0.7185, 0.7148, 0.7159]
yelp_ndcg_rand = [0.4242, 0.4362, 0.4408, 0.4418, 0.4437]

yelp_hr = [0.7245, 0.7263, 0.7343, 0.7377, 0.7382, 0.7473, 0.7432, 0.7414, 0.7423, 0.7506] # 0.7432, 0.7414, 0.7423
yelp_ndcg = [0.4362, 0.4402, 0.4445, 0.4497, 0.4544, 0.4579, 0.4609, 0.4575, 0.4624, 0.4666] # 0.4609, 0.4575, 0.4624

pp_hr = [0.3619, 0.3460, 0.3361, 0.3276, 0.3226, 0.3199, 0.3139, 0.3104, 0.3003, 0.3006] # 0.3139 0.3104 0.3003
pp_ndcg = [0.2300, 0.2181, 0.2077, 0.2046, 0.1999, 0.1949, 0.1926, 0.1877, 0.1818, 0.1794] # 0.1926 0.1877 0.1818

def plot_performance(ml_data, yelp_data, pp_data, datatype):
    x_labels = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x_labels, ml_data, "-o", label = 'MovieLens 1M')
    plt.plot(x_labels, yelp_data, "-o", label = 'Yelp')
    plt.plot(x_labels, pp_data, "-o", label = 'Amazon Prime Pantry')
    plt.title(f"{datatype} performance of mixed datasets")
    plt.xlabel('Percentage of longtail data mixed')
    plt.ylabel(datatype)
    for i, v in enumerate(ml_data):
        ax.annotate(str(v), xy=(i,v), xytext=(-7,7), textcoords='offset points')
    for i, v in enumerate(yelp_data):
        ax.annotate(str(v), xy=(i,v), xytext=(-7,7), textcoords='offset points')
    for i, v in enumerate(pp_data):
        ax.annotate(str(v), xy=(i,v), xytext=(-7,7), textcoords='offset points')
    plt.legend()
    plt.show()

ml_hot = [479843, 517152, 552738, 586181, 618039, 646365, 670732, 691755, 708151]
ml_lt = [210916, 220892, 230303, 239101, 247404, 255141, 261659, 267139, 271203]

yelp_hot = [325991, 348176, 369551, 390301, 411336, 431732, 451311, 469981, 487711]
yelp_lt = [137498, 145354, 153181, 161099, 168377, 175545, 182785, 189759, 196301]

pp_hot = [241534, 251613, 260331, 268525, 275616, 281666, 286346, 289485, 291118]
pp_lt = [136984, 143014, 148451, 153532, 158025, 161843, 164861, 166962, 168253]

yelp_lesser_hot = [310720, 317723, 324765, 331787, 338872, 346019, 353032, 360033, 367053, 374207]
yelp_lesser_lt = [132268, 134875, 137443, 140031, 142556, 145019, 147616, 150225, 152815, 155286]

def plot_mixdata(hot_data, lt_data, dataset):
    x_labels = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x_labels, hot_data, "-o", label = 'Hot sample points')
    plt.plot(x_labels, lt_data, "-o", label = 'Lt sample points')
    plt.title(f"Number of different sample points in {dataset} dataset")
    plt.xlabel('Percentage of longtail data mixed')
    plt.ylabel('Samples')
    for i, v in enumerate(hot_data):
        ax.annotate(str(v), xy=(i,v), xytext=(-7,7), textcoords='offset points')
    for i, v in enumerate(lt_data):
        ax.annotate(str(v), xy=(i,v), xytext=(-7,7), textcoords='offset points')
    plt.legend()
    plt.show()

plot_mixdata(yelp_lesser_hot, yelp_lesser_lt, 'Yelp')