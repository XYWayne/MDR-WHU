# Research Log

## Outline
1. Models 
2. Parameters for experiments
3. Data overview and preprocess
4. Results and experiment log
---

### Models 
Acknowledgment: models described below are folked from Xiangnan He's [repo](https://github.com/hexiangnan/neural_collaborative_filtering).  
I've updated the codes so that they work on the latest versions of Keras and Python.  

---

### Parameters for experiments
In these experiments we mainly use NeuMF for our cases, however GMF and MLP may also be run to serve as benchmarks. As from the github page of the above hyperlink, to run an example training:
```
python3 NeuMF.py --dataset ml-1m --epochs 20 --batch_size 256 --num_factors 8 --layers [64,32,16,8] --reg_mf 0 --reg_layers [0,0,0,0] --num_neg 4 --lr 0.001 --learner adam --verbose 1 --out 1
```
---

### Data  overview and preprocess
#### Original Datasets
I currently have 3 datasets for this experiment: [Pinterest, MovieLens, Yelp](https://github.com/hexiangnan/adversarial_personalized_ranking), and [Amazon Prime Pantry](https://jmcauley.ucsd.edu/data/amazon/). 

The original dataset contains:

* **train.rating**:  
Each line is a training example: `userID\t itemID\t rating\t timestamp`

* **test.rating**:  
Each line is a testing example: `userID\t itemID\t rating\t timestamp`

* **test.negative**:  
Each line is in the format: `(userID,itemID)\t negativeItemID1\t negativeItemID2\t ...`

In order to study the effect of training on a data set that consists of a "hot" part and a "longtail" part, we can first get a visualization of our datasets. Note the we have removed the userIDs with frequency 1 from the raw dataset. Below are some statistics of the above datasets:

|                          | MovieLens-1M  | Pinterests-20     |   Yelp    |   Prime Pantry   |
| :---:                    |    :----:     |       :---:       |  :----:   |     :---:        |
| Training Samples         | 994169        |1445622            |705994     |460800            |
| Testing Samples          | 6040          |55187              |25677      |10009             |
| Negative Samples         | 6040          |55187              |25677      |10009             |

Now, if we want to conduct hot-longtail analysis, we should first see the distribution of user frequency:

|               | MovieLens-1M  | Pinterests-20     |   Yelp   |   Prime Pantry   |
| :---:         |    :----:     |       :---:       |  :----:  |     :---:        |
| Count         | 6040          |55187              |25677     |10009             |
| Mean          | 165           |26                 |27        |47                |
| Std           | 192           |7                  |42        |156               |
| Min           | 19            |14                 |9         |2                 |
| 25 percentile | 43            |21                 |11        |6                 |
| 50 percentile | 95            |24                 |15        |17                |
| 75 percentile | 207           |29                 |27        |43                |
| Max           | 2313          |136                |1175      |6537              |

Below are the visualizations of the datasets' userID distributions:  
* MovieLens:
<img src = "https://user-images.githubusercontent.com/59850013/183307329-585d32ed-55fe-434b-97ce-a45fbff70e70.png" width=75% height=75%>

* Pinterests:
<img src = "https://user-images.githubusercontent.com/59850013/183307345-fe7ae6ec-cb5a-4a02-a488-d8e1605a9513.png" width=75% height=75%>

* Yelp:
<img src = "https://user-images.githubusercontent.com/59850013/183307355-5b54e272-d285-4495-bd41-5c74a478383f.png" width=75% height=75%>

* Prime Pantry:
<img src = "https://user-images.githubusercontent.com/59850013/183307363-5ae1c9ed-ef6b-4803-985b-5555058a8672.png" width=75% height=75%>

**Note:**  
From the plots we can see that among these datasets, **MovieLens, Yelp, and Prime Pantry** have obvious hot-longtail distributions. Thus, in order to study the hot-longtail data structure, we only conduct further experiments on these 3 datasets.

#### Splited Datasets
In order to study the effect of training hot-longtail data structures, we hereby split the original datasets into the hot part and the long tail part based on the user frequency. **Any userID with frequency higher than the 75 percentile is considered to be in the hot part, and those who are below the threshold are considered to be in the ongtail part.** Note that there is still a debate over the choice of the threshold.

The splited dataset contains:

* **train.hot.rating**:  
Each line is a training example from the hot part: `userID\t itemID\t rating\t timestamp`

* **test.hot.rating**:  
Each line is a testing example from the hot part: `userID\t itemID\t rating\t timestamp`

* **test.hot.negative**:  
Each line is an instance of negative samples with userID in the hot part: `(userID,itemID)\t negativeItemID1\t negativeItemID2\t ...`

* **train.lt.rating**:  
Each line is a training example from the longtail part: `userID\t itemID\t rating\t timestamp`

* **test.lt.rating**:  
Each line is a testing example from the longtail part: `userID\t itemID\t rating\t timestamp`

* **test.lt.negative**:  
Each line is an instance of negative samples with userID in the longtail part: `(userID,itemID)\t negativeItemID1\t negativeItemID2\t ...`

Here is the data distribution after spliting:

|                               | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:                         |    :----:     |  :----:   |     :---:        |
| Training Samples(hot)         | 630603        |433378     |362401            |
| Testing Samples(hot)          | 1511          |6454       |2500              |
| Negative Samples(hot)         | 1511          |6454       |2500              |
| Training Samples(lt)          | 354566        |272616     |98983             |
| Testing Samples(lt)           | 4529          |19223      |6919              |
| Negative Samples(lt)          | 4529          |19223      |6919              |

---
### Results and experiment log
---
### Benchmarks
#### Benchmark I
Benchmark I is produced by training and testing on the original datasets.
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |0.6816         |0.7506     |0.3006            |
| NDCG    |0.4053         |0.4666     |0.1794            |

#### Benchmark II
Benchmark II is produced by training on original datasets and testing on the splited datasets.
|                   | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:             |    :----:     |  :----:   |     :---:        |
| HR(hot)           |0.5096         |0.7008     |0.3762            |
| HR(longtail)      |0.7437         |0.7678     |0.2730            |
| NDCG(hot)         |0.2715         |0.4041     |0.2406              |
| NDCG(longtail)    |0.4515         |0.4910     |0.1672              |

---
### Hot-longtail data structure performance
#### Hot part performances
Hot part performances are produced by training and testing on the hot part datasets.
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |0.4990         |0.7099     |0.3750            |
| NDCG    |0.2647         |0.4124     |0.2384              |

#### Longtail part performances
Longtail part performances are produced by training and testing on the longtail part datasets.
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |0.7227         |0.6128     |0.2513            |
| NDCG    |0.4379         |0.3817     |0.1477            |

---
### Mixed data structure performance
#### To further investigate the subject, we decide to blend in the examples from the longtail part with the hot part by percentage.
100% hot part + 10% longtail part
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |         |     |            |
| NDCG    |         |     |              |

100% hot part + 20% longtail part
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |         |     |            |
| NDCG    |         |     |              |

100% hot part + 30% longtail part
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |         |     |            |
| NDCG    |         |     |              |

100% hot part + 50% longtail part
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |         |     |            |
| NDCG    |         |     |              |

100% hot part + 70% longtail part
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |         |     |            |
| NDCG    |         |     |              |

100% hot part + 80% longtail part
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |         |     |            |
| NDCG    |         |     |              |

100% hot part + 90% longtail part
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |         |     |            |
| NDCG    |         |     |              |

100% hot part + 100% longtail part (i.e., the benchmark I)
|         | MovieLens-1M  |   Yelp    |   Prime Pantry   |
| :---:   |    :----:     |  :----:   |     :---:        |
| HR      |         |     |            |
| NDCG    |         |     |              |
