import matplotlib.pyplot as plt

x_labels = ['10%', '20%', '30%', '40%', '50%', '60%', '70%'] # ', '40%', '50%', '60%', '70%', '80%', '90%', '100%'
ml_hr = [0.5436, 0.5801, 0.5940, 0.6086, 0.6248, 0.6415, 0.6520] # 0.6612, 
ml_ndcg = [0.2978, 0.3204, 0.3310, 0.3477, 0.3517, 0.3708, 0.3788] # 0.3889

yelp_hr = [0.7245, 0.7263, 0.7343, 0.7377, 0.7382, 0.7473] # 0.7432, 0.7414
yelp_ndcg = [0.4362, 0.4402, 0.4445, 0.4497, 0.4544, 0.4579] # 0.4609, 0.4575

pp_hr = [0.3619, 0.3460, 0.3361, 0.3276, 0.3226, 0.3199]
pp_ndcg = [0.2300, 0.2181, 0.2077, 0.2046, 0.1999, 0.1949]

plt.plot(x_labels, ml_hr, "-o", label = 'MovieLens 1M')
plt.plot(x_labels, yelp_hr, "-o", label = 'Yelp')
plt.plot(x_labels, pp_hr, "-o", label = 'Amazon Prime Pantry')
plt.set_xticklabels(x_labels)
plt.title("HR performance of mixed datasets")
plt.xlabel('Percentage of longtail data mixed')
plt.ylabel('HR')
plt.legend()
plt.show()