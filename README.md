# MDR

## Outline
1. Models 
2. Parameters for experiments
3. Data overview and preprocess
4. Results and experiment log
---

### Models
Note: models described here are folked from Xiangnan He's [repo](https://github.com/hexiangnan/neural_collaborative_filtering).
In this experiments we mainly use NeuMF for our cases, however GMF and MLP may also be run to serve as benchmarks.
---

### Parameters for experiments
As from the github page of the above hyperlink, to run an example training:
```
python3 NeuMF.py --dataset ml-1m --epochs 20 --batch_size 256 --num_factors 8 --layers [64,32,16,8] --reg_mf 0 --reg_layers [0,0,0,0] --num_neg 4 --lr 0.001 --learner adam --verbose 1 --out 1
```
---

### Data  overview and preprocess
I currently have 3 datasets for this experiment: [Pinterest, MovieLens, Yelp](https://github.com/hexiangnan/adversarial_personalized_ranking), and [Amazon Prime Pantry](https://jmcauley.ucsd.edu/data/amazon/). 

In order to study the effect of training on a data set that consists of a "hot" part and a "longtail" part, we can first get a nice visualization of out datasets. Below are some statistics of the above datasets:

|               | MovieLens-1M  | Pinterests-20     |   Yelp   |   Prime Pantry   |
| :---:         |    :----:     |       :---:       |  :----:  |     :---:        |
| Training Samples         | 994169        |1445622           |705994     |461336         |
| Testing Samples          | 6040          |55187             |25677      |10812          |
| Negative Samples         | 6040          |55187             |25677      |9467           |

Now, if we want to conduct hot-longtail analysis, we should first see the distribution of user frequency:

|               | MovieLens-1M  | Pinterests-20     |   Yelp   |   Prime Pantry   |
| :---:         |    :----:     |       :---:       |  :----:  |     :---:        |
| Count         | 6040          |55187              |25677     |10814             |
| Mean          | 165           |26                 |27        |43                |
| Std           | 192           |7                  |42        |151               |
| Min           | 19            |14                 |9         |1                 |
| 25 percentile | 43            |21                 |11        |5                 |
| 50 percentile | 95            |24                 |15        |15                |
| 75 percentile | 207           |29                 |27        |39                |
| Max           | 2313          |136                |1175      |6537              |
