import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression, LogisticRegression
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, mean_squared_error, r2_score
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('final_dataset.csv')
data = data.drop(['date', 'hour_datetime'], axis=1)


X = data.drop('is_alarm', axis=1)
y = data['is_alarm']

tscv = TimeSeriesSplit(n_splits=5)
print(tscv)

accuracies1 = []
mses1 = []
conf_matrices1 = []

model1 = LinearRegression(positive=True, fit_intercept=False)
i = 1

# Linear Regression
for train_index, test_index in tscv.split(X):
    print(i)
    i += 1
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    print(len(X_train))
    print(len(y_train))
    print(len(X_test))
    print(len(y_test))

    model1.fit(X_train, y_train)

    accuracy = model1.score(X_test, y_test)
    accuracies1.append(accuracy)

    y_pred = model1.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mses1.append(mse)

mean_accuracy = sum(accuracies1) / len(accuracies1)
mean_mse = sum(mses1) / len(mses1)

print("accuracy: {:.2f}%".format(mean_accuracy * 100))
print("MSE: {:.2f}".format(mean_mse))

joblib.dump(model1, 'linear_regression_model_encoded_test.pkl')


accuracies2 = []
precisions = []
recalls = []
mses2 = []
r2_scores = []
conf_matrices2 = []

model2 = LogisticRegression(max_iter=50000, class_weight='balanced', solver='newton-cg', C=np.logspace(-4, 4, 2)[1], penalty='l2', tol=0.000001)

i = 1
#Logistic Regression
for train_index, test_index in tscv.split(X):
    print(i)
    i += 1
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    print(len(X_train))
    print(len(y_train))
    print(len(X_test))
    print(len(y_test))

    model2.fit(X_train, y_train)

    y_pred = model2.predict(X_test)

    accuracy = model2.score(X_test, y_test)
    accuracies2.append(accuracy)

    conf_matrix = confusion_matrix(y_test, y_pred)
    conf_matrices2.append(conf_matrix)

    precision = precision_score(y_test, y_pred)
    precisions.append(precision)

    recall = recall_score(y_test, y_pred)
    recalls.append(recall)

    mse = mean_squared_error(y_test, y_pred)
    mses2.append(mse)

    r2 = r2_score(y_test, y_pred)
    r2_scores.append(r2)

mean_accuracy = sum(accuracies2) / len(accuracies2)
mean_precision = sum(precisions) / len(precisions)
mean_recall = sum(recalls) / len(recalls)
mean_mse = sum(mses2) / len(mses2)
mean_r2 = sum(r2_scores) / len(r2_scores)

print("Accuracy: {:.2f}%".format(mean_accuracy * 100))
print("Precision: {:.2f}".format(mean_precision))
print("Recall: {:.2f}".format(mean_recall))
print("MSE: {:.2f}".format(mean_mse))
print("R-squared: {:.2f}".format(mean_r2))

class_labels = ['Not Alarm', 'Alarm']

for i, conf_matrix in enumerate(conf_matrices2):
    print(f"Confusion Matrix for Alarms (LogisticRegression){i+1}:")
    print(conf_matrix)

    sns.heatmap(conf_matrix,
                annot=True,
                fmt='g',
                xticklabels=class_labels,
                yticklabels=class_labels)
    plt.ylabel('Prediction', fontsize=13)
    plt.xlabel('Actual', fontsize=13)
    plt.title(f'Confusion Matrix - Iterration {i+1}', fontsize=17)
    plt.show()

joblib.dump(model2, 'logistic_regression_model_encoded.pkl')





