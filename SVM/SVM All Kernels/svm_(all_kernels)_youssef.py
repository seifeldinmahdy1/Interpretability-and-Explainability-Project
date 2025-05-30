# -*- coding: utf-8 -*-
"""SVM (ALL KERNELS) youssef.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aksa1wag3kk28DqhwIfAyGNtKKXDkJlp
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

data = load_breast_cancer()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm_rbf = SVC(kernel='rbf')
svm_rbf.fit(X_train_scaled, y_train)

y_pred = svm_rbf.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("RBF Kernel:")
print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"F1-score: {f1 * 100:.2f}%")
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=data.target_names)
disp.plot()
plt.show()

cv_scores = cross_val_score(svm_rbf, X_train_scaled, y_train, cv=5)
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean CV score: {cv_scores.mean()*100:.2f}%")

svm_linear = SVC(kernel='linear')
svm_linear.fit(X_train_scaled, y_train)
y_pred_linear = svm_linear.predict(X_test_scaled)

accuracy_linear = accuracy_score(y_test, y_pred_linear)
precision_linear = precision_score(y_test, y_pred_linear)
recall_linear = recall_score(y_test, y_pred_linear)
f1_linear = f1_score(y_test, y_pred_linear)
conf_matrix_linear = confusion_matrix(y_test, y_pred_linear)

print("Linear Kernel:")
print(f"Accuracy: {accuracy_linear * 100:.2f}%")
print(f"Precision: {precision_linear * 100:.2f}%")
print(f"Recall: {recall_linear * 100:.2f}%")
print(f"F1-score: {f1_linear * 100:.2f}%")
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_linear, display_labels=data.target_names)
disp.plot()
plt.show()

cv_scores_linear = cross_val_score(svm_linear, X_train_scaled, y_train, cv=5)
print(f"Cross-validation scores (Linear): {cv_scores_linear}")
print(f"Mean CV score (Linear): {cv_scores_linear.mean()*100:.2f} %")

svm_poly = SVC(kernel='poly')
svm_poly.fit(X_train_scaled, y_train)
y_pred_poly = svm_poly.predict(X_test_scaled)

accuracy_poly = accuracy_score(y_test, y_pred_poly)
precision_poly = precision_score(y_test, y_pred_poly)
recall_poly = recall_score(y_test, y_pred_poly)
f1_poly = f1_score(y_test, y_pred_poly)
conf_matrix_poly = confusion_matrix(y_test, y_pred_poly)

print("Polynomial Kernel:")
print(f"Accuracy: {accuracy_poly * 100:.2f}%")
print(f"Precision: {precision_poly * 100:.2f}%")
print(f"Recall: {recall_poly * 100:.2f}%")
print(f"F1-score: {f1_poly * 100:.2f}%")
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_poly, display_labels=data.target_names)
disp.plot()
plt.show()

cv_scores_poly = cross_val_score(svm_poly, X_train_scaled, y_train, cv=5)
print(f"Cross-validation scores (Polynomial): {cv_scores_poly}")
print(f"Mean CV score (Polynomial): {cv_scores_poly.mean()*100:.2f}%")

svm_sigmoid = SVC(kernel='sigmoid')
svm_sigmoid.fit(X_train_scaled, y_train)

y_pred_sigmoid = svm_sigmoid.predict(X_test_scaled)
accuracy_sigmoid = accuracy_score(y_test, y_pred_sigmoid)
precision_sigmoid = precision_score(y_test, y_pred_sigmoid)
recall_sigmoid = recall_score(y_test, y_pred_sigmoid)
f1_sigmoid = f1_score(y_test, y_pred_sigmoid)
conf_matrix_sigmoid = confusion_matrix(y_test, y_pred_sigmoid)

print("Sigmoid Kernel:")
print(f"Accuracy: {accuracy_sigmoid * 100:.2f}%")
print(f"Precision: {precision_sigmoid * 100:.2f}%")
print(f"Recall: {recall_sigmoid * 100:.2f}%")
print(f"F1-score: {f1_sigmoid * 100:.2f}%")
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_sigmoid, display_labels=data.target_names)
disp.plot()
plt.show()

cv_scores_sigmoid = cross_val_score(svm_sigmoid, X_train_scaled, y_train, cv=5)
print(f"Cross-validation scores (Sigmoid): {cv_scores_sigmoid}")
print(f"Mean CV score (Sigmoid): {cv_scores_sigmoid.mean()*100:.2f}%")

"""# Best Performing Kernel:

The RBF kernel performed the best, achieving high accuracy and F1-score.
"""