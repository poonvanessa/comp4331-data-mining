#!/usr/bin/python

import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

digits = datasets.load_digits()

images_and_labels = list(zip(digits.images, digits.target))

n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Decision Tree
# classifier = DecisionTreeClassifier(criterion="entropy",max_depth=5)

# KNN, SVM, Random Forest
classifier = KNeighborsClassifier()
classifier = svm.SVC(gamma=0.001)
classifier = RandomForestClassifier()

# Multilayer perception
# classifier = MLPClassifier(alpha=1)  
#      
# classifier = GaussianNB()

classifier.fit(data[:n_samples // 2], digits.target[:n_samples // 2])
expected = digits.target[n_samples // 2:]
predicted = classifier.predict(data[n_samples // 2:])

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))