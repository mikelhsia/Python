import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from sklearn import tree
import pydotplus
from sklearn.externals.six import StringIO
from IPython.display import Image, display
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from itertools import product

import matplotlib.pyplot as plt

import tushare as ts

target = ['change_rate_quant']
predictors = ['PCF', 'turnover_ratio', 'PE_rate', 'PB_rate', 'PS_rate', 'pmi', 'pmi_rate', 'leading_idx_rate', 'M1_rate',
              'M2_rate', 'CPI_rate', 'GDP_rate', 'LOAN6MONTH', 'LARGEFINANCIAL', 'SMALLFINANCIAL', 'dcg', 'URUR']

def get_bins (srs, frac= []):
    arr = []

    if (frac == []) :
        raise Exception('frac array is empty. Please specify quantile detail');
    bn = srs.quantile(frac)
    arr = [pd.Series.min(srs)] + [bn.iloc[x] for x in range(pd.Series.count(bn))] + [pd.Series.max(srs)]
    return arr

df = ts.get_hist_data('600848')

# TODO: Moving windows and rolling
df['change_rate'] = df['close'].pct_change()
cats = pd.cut(df['change_rate'], get_bins(df['change_rate'], [0.25, 0.75]))

# print(cats.values)
# print(cats.values.codes)
# print(cats.values.categories)

df['change_rate_quant'] = cats.values.codes
print(df['change_rate_quant'])

# TODO: Find a way to download all macro financial data

# TODO: Apply Decision Tree modeling
train = df.sample(frac=0.7, random_state=1)
test = df[df.index.isin(train.index)==False].copy()

X_train = train[predictors]
X_test = test[predictors]
y_train = train[target]
y_test = test[target]

# 建立决策树模型
decisionTree_res = tree.DecisionTreeClassifier(max_depth=10, min_samples_leaf=5, min_samples_split=10)
decisionTree_res.fit(X_train, y_train)
# 以上是决策树建立的代码，我们用CART的方法用‘gini值’确定叶数据纯度，并要求节点最少应该有10个数据，每片叶最少有5个数据。
# 决策树模型的主要参数有：
# criterion: 决定判断节点纯度的方法。目前sklearn支持”gini”和”entropy”两种，分别对应用基尼指数和信息增益的CART和ID3两种算法，默认算法是“gini”。
# max_depth: 最大树深度，达到最大数深度即停止分叉，最常用的约束，默认值为None
# spliter: 决定如何分叉每个节点。目前sklearn支持“best”和“random”两种，指的是选取特征的最优分叉点分叉还是随机分叉点分叉，默认值是“best”
# max_features: 使用特征值的最大数量，默认为None
# max_leaf_nodes: 叶节点的数量，默认值为None
# min_impurity_split: 最小纯度门槛，假如纯度小于最小纯度，则会继续切分，默认值为None
# min_samples_leaf: 最小叶数据，达到则不再分叉，默认值为1
# min_samples_split: 最小节点数据，达到则不再分叉，默认值是2

# 接下来进行预测
f = StringIO()
tree.export_graphviz(decisionTree_res, out_file=f)
graph = pydotplus.graph_from_dot_data(f.getvalue())
graph.write_png('dtree3.png')
display(Image(graph.create_png()))

# TODO: Analysis
# 精度很差，只是略高于一半而已。简单的决策树过于基础，识别能力有限，用于预测股市显然很一般。
# 不过决策树是很多机器学习方法的基石，其改进模型往往会有较好表现。此外决策树便于可视化，他的产生的分布图可以用于数据研究，例如决策树的每一片
# 叶都是相对比较纯净的数据集，使用者可以抽出一些纯度比较高的叶来研究为何在训练集中这些叶上的数据集纯度较高，从而发现新规律。

# 得到预测结果
prediction = decisionTree_res.predict(X_test)

# 输出预测结果统计
print(confusion_matrix(prediction, y_test))
print(classification_report(y_test, prediction, digits=3))
print("The table finished")