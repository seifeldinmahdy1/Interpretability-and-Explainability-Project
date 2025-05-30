# -*- coding: utf-8 -*-
"""Seif El Din Mahdy_SVM-LDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1npcTZuXIS_28VJCpU9rXxoSE4i3dqmSD
"""

!pip install alibi

!pip install lime shap

!pip install eli5

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, roc_curve, f1_score
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, classification_report, precision_recall_curve
from sklearn.model_selection import learning_curve, validation_curve
from sklearn.inspection import partial_dependence, PartialDependenceDisplay
from sklearn.feature_selection import RFE
from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.inspection import permutation_importance
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import shap
import lime
import lime.lime_tabular
import eli5
from eli5.sklearn import PermutationImportance
from alibi.explainers import ALE
from alibi.explainers import plot_ale
import matplotlib.pyplot as plt

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

X_scaled.head()

X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, train_size=399, test_size=170, stratify=y, random_state=32)

svm = SVC(kernel='rbf', probability=True, random_state=42)
svm.fit(X_train, y_train)

lda = LDA(n_components=1)
X_train_lda = lda.fit_transform(X_train, y_train)
X_val_lda = lda.transform(X_val)

svm_lda = SVC(kernel='rbf', probability=True, random_state=42)
svm_lda.fit(X_train_lda, y_train)

y_pred = svm.predict(X_val)
y_proba = svm.predict_proba(X_val)[:, 1]

y_pred_lda = svm_lda.predict(X_val_lda)
y_proba_lda = svm_lda.predict_proba(X_val_lda)[:, 1]

cm = confusion_matrix(y_val, y_pred_lda, labels=[1, 0])
tn, fp, fn, tp = cm.ravel()

accuracy = accuracy_score(y_val, y_pred_lda)
precision = precision_score(y_val, y_pred_lda, pos_label=0)
recall = recall_score(y_val, y_pred_lda, pos_label=0)
f1 = f1_score(y_val, y_pred_lda)
report = classification_report(y_val, y_pred_lda, target_names=data.target_names)

print("Performance Metrics:")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

print("\nClassification Report:")
print(report)

train_sizes, train_scores, val_scores = learning_curve(
    SVC(kernel='rbf', probability=True, random_state=42),
    X_train_lda, y_train,
    cv=5, scoring='accuracy',
    train_sizes=np.linspace(0.1, 1.0, 10),
    n_jobs=-1
)

train_scores_mean = np.mean(train_scores, axis=1)
val_scores_mean = np.mean(val_scores, axis=1)

plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_scores_mean, label='Training score')
plt.plot(train_sizes, val_scores_mean, label='Cross-validation score')
plt.title('Learning Curve for SVM with LDA')
plt.xlabel('Training Set Size')
plt.ylabel('Accuracy')
plt.legend(loc='best')
plt.grid(True)
plt.show()

param_range = np.logspace(-3, 3, 7)
train_scores, val_scores = validation_curve(
    SVC(kernel='rbf', probability=True, random_state=42),
    X_train_lda, y_train,
    param_name='C', param_range=param_range,
    cv=5, scoring='accuracy',
    n_jobs=-1
)

train_scores_mean = np.mean(train_scores, axis=1)
val_scores_mean = np.mean(val_scores, axis=1)

plt.figure(figsize=(10, 6))
plt.semilogx(param_range, train_scores_mean, label='Training score')
plt.semilogx(param_range, val_scores_mean, label='Cross-validation score')
plt.title('Validation Curve for SVM (Parameter: C)')
plt.xlabel('C (Regularization Parameter)')
plt.ylabel('Accuracy')
plt.legend(loc='best')
plt.grid(True)
plt.show()

cm = confusion_matrix(y_val, y_pred_lda)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=data.target_names)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

fpr, tpr, _ = roc_curve(y_val == 1, y_proba_lda)
roc_auc = roc_auc_score(y_val == 1, y_proba_lda)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for SVM-LDA')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()

precision, recall, _ = precision_recall_curve(y_val, y_proba_lda)
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, label='Precision-Recall Curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve for SVM-LDA')
plt.legend(loc='lower left')
plt.grid(True)
plt.show()

coefficients = pd.Series(lda.coef_[0], index=X.columns)
coefficients_sorted = coefficients.sort_values(key=abs, ascending=False)

plt.figure(figsize=(12, 6))
coefficients_sorted.plot(kind='bar', color='steelblue')
plt.title('LDA Coefficients (Feature Importance)')
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.xticks(rotation=75)
plt.grid(True)
plt.tight_layout()
plt.show()

x_range = np.linspace(X_train_lda.min()-1, X_train_lda.max()+1, 500).reshape(-1, 1)
y_proba = svm_lda.predict_proba(x_range)[:, 1]

plt.figure(figsize=(10, 6))

plt.scatter(X_train_lda[y_train==0], np.zeros_like(X_train_lda[y_train==0]),color='blue', label='Class 0', alpha=0.6)
plt.scatter(X_train_lda[y_train==1], np.zeros_like(X_train_lda[y_train==1]),color='red', label='Class 1', alpha=0.6)

plt.plot(x_range, y_proba, color='black', label='SVM Prob(Class 1)', linewidth=2)
plt.axvline(x=x_range[np.argmin(np.abs(y_proba - 0.5))], color='green', linestyle='--', label='Decision Boundary')

plt.title('LDA Projection with SVM Decision Boundary')
plt.xlabel('LDA 1D Projection')
plt.yticks([])
plt.legend()
plt.grid(True)
plt.show()

from eli5.sklearn import PermutationImportance
import eli5

perm = PermutationImportance(svm, random_state=42).fit(X_train, y_train)
eli5.show_weights(perm, feature_names=X.columns.tolist())

for feature in X.columns.tolist():
    PartialDependenceDisplay.from_estimator(svm, X_val, features=[feature], target=0, feature_names=X.columns.tolist())
    plt.title("PDP")
    plt.show()

for feature in X.columns.tolist():
    PartialDependenceDisplay.from_estimator(svm, X_val, features=[feature], target=0, kind='individual')
    plt.title("ICE")
    plt.show()

proba_fun_svm = svm.predict_proba
proba_ale_svm = ALE(proba_fun_svm, feature_names=X_train.columns.tolist()[0:6], target_names=data.target_names)
proba_exp_svm = proba_ale_svm.explain(X_train.values)

plot_ale(proba_exp_svm, n_cols=3, fig_kw={'figwidth': 12, 'figheight': 6}, sharey=True)
plt.show()

result = permutation_importance(svm, X_val, y_val, n_repeats=10, random_state=42,scoring='accuracy')

sorted_idx = result.importances_mean.argsort()

plt.figure(figsize=(10, 6))
plt.barh([X.columns[i] for i in sorted_idx], result.importances_mean[sorted_idx])
plt.title("Permutation Feature Importance - SVM")
plt.tight_layout()
plt.show()

baseline = cross_val_score(svm, X_train, y_train, cv=5).mean()

lofo_scores = {}
for col in X_train.columns:
    X_lofo = X_train.drop(columns=[col])
    score = cross_val_score(svm, X_lofo, y_train, cv=5).mean()
    lofo_scores[col] = baseline - score

lofo_df = pd.Series(lofo_scores).sort_values(ascending=False)

plt.figure(figsize=(10, 6))
lofo_df.plot(kind='barh')
plt.title("LOFO Importance - SVM")
plt.tight_layout()
plt.show()

svm_preds = svm.predict(X_train)
surrogate = DecisionTreeClassifier(max_depth=3, random_state=42)
surrogate.fit(X_train, svm_preds)

plt.figure(figsize=(12, 6), dpi=150)
tree.plot_tree(surrogate, feature_names=X.columns.tolist(), filled=True, rounded=True, class_names=data.target_names)
plt.title("Global Surrogate Tree - SVM")
plt.tight_layout()
plt.show()

!pip install artemis

!pip install pyartemis

from artemis.interactions_methods.model_agnostic import FriedmanHStatisticMethod
import random

random.seed(8)
X_exp = random.choices(X_train.values.tolist(), k=100)
X_exp = pd.DataFrame(X_exp, columns=X.columns)

h_stat = FriedmanHStatisticMethod()
h_stat.fit(svm, X_exp)

fig, ax = plt.subplots(figsize=(12, 4))
h_stat.plot('bar_chart_ova',ax=ax)

fig, ax = plt.subplots(figsize=(10, 4))
h_stat.plot(vis_type='bar_chart',ax=ax)

h_stat.plot()

explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=np.array(X_train),
    feature_names=X.columns.tolist(),
    class_names=data.target_names.tolist(),
    mode='classification',
    discretize_continuous=True
)

exp = explainer.explain_instance(data_row=X_val.iloc[0],predict_fn=svm.predict_proba,num_features=len(X.columns))
exp.show_in_notebook(show_table=True, show_all=False)

feature_names = X.columns

background_data = shap.sample(X_train, 100)

explainer = shap.KernelExplainer(svm.predict_proba, background_data)

shap_values = explainer.shap_values(X_val)

plt.figure()
shap.summary_plot(shap_values[:, :, 1], X_val, feature_names=feature_names, show=True)
plt.show()

explanation = shap.Explanation(
    values=shap_values[:, :, 1],
    base_values=explainer.expected_value[1],
    data=X_val,
    feature_names=feature_names
)

num_features = len(feature_names)
plt.figure()
shap.plots.bar(explanation, max_display=num_features, show=True)
plt.close()

plt.figure()
shap.plots.waterfall(explanation[0], max_display=num_features, show=True)
plt.close()

plt.figure()
shap.plots.waterfall(explanation[1], max_display=num_features, show=True)
plt.close()

plt.figure()
shap.plots.heatmap(explanation, max_display=num_features, show=True)
plt.close()