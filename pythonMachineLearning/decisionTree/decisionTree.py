from sklearn.datasets import load_iris
from sklearn import tree
import pydotplus
from sklearn.externals.six import StringIO
from IPython.display import Image, display

# load_iris 是 sklearn的测试数据， 在这里用来做决策树演示
iris = load_iris()
# print(iris)

# 建立最大深度为2的决策树，并用测试数据来训练这棵树
clf = tree.DecisionTreeClassifier(max_depth=2)
clf = clf.fit(iris.data, iris.target)
# print("iris.target:{}".format(iris.data))
# print("iris.target:{}".format(iris.target))

# 假设我们要预测第10个样本的值
sample_idx = 111

# 第10个样本的各个属性，在这里可以看到有4个属性
print(iris.data[sample_idx])

# 预测，结果是第二类
prediction = clf.predict(iris.data[sample_idx:sample_idx+1])
print(prediction)

# 真实值也是第二类，结果正确
truth = iris.target[sample_idx]
print(truth)

# 用于观察结果的可能性，由图可知因为这个项属于0，1，2的概率分别为0，0.0222，0.978，属于2类的概率最大，决策树把它归入2类
class_probabilities = clf.predict_proba(iris.data[sample_idx:sample_idx+1])
print(class_probabilities)

# 用于展示不同因子的重要性，此处可知第4个因子决定了这一判断，重要性为100%，其他因子未参与判断
print(clf.feature_importances_)

# 建立缓存变量f
f = StringIO()
# 把决策树clf的图形结果输出，扔进缓存f中
tree.export_graphviz(clf, out_file=f)
# 取出缓存，画图
graph = pydotplus.graph_from_dot_data(f.getvalue())
# 将图片存进本地
graph.write_png('dtree2.png')
# 画出决策树，也可以用标注的代码画出保存在本地的png图片
# display(Image(filename='dtree2.png'))
display(Image(graph.create_png()))