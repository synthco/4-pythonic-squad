import pandas as pd
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import TimeSeriesSplit
import joblib
from sklearn.metrics import accuracy_score, precision_score, mean_squared_error, r2_score

import xgboost as xgb

data = pd.read_csv(
    '/Users/matvejzasadko/Downloads/All/Python_cource_project/4-pythonic-squad/source/MergeData/final_dataset_v3.csv')
data = data.drop(['date', 'hour_datetime'], axis=1)

X = data.drop('is_alarm', axis=1)
y = data['is_alarm']

tscv = TimeSeriesSplit(n_splits=5)
print(tscv)


mses = []
r2_scores = []
accuracies = []
precisions = []

model11 = ExtraTreesClassifier()

i = 1

# Train ExtraTreesClassifier
for train_index, test_index in tscv.split(X):
    print(i)
    i += 1
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    print(len(X_train))
    print(len(y_train))
    print(len(X_test))
    print(len(y_test))

    model11.fit(X_train, y_train)

    y_pred = model11.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mses.append(mse)

    r2 = r2_score(y_test, y_pred)
    r2_scores.append(r2)

    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)

    precision = precision_score(y_test, y_pred)
    precisions.append(precision)

mean_mse = sum(mses) / len(mses)
mean_r2 = sum(r2_scores) / len(r2_scores)
mean_accuracy = sum(accuracies) / len(accuracies)
mean_precision = sum(precisions) / len(precisions)

print('ExtraTreesClassifier model')
print("MSE: {:.2f}".format(mean_mse))
print("R-squared: {:.2f}".format(mean_r2))
print("Accuracy: {:.2f}%".format(mean_accuracy * 100))
print("Precision: {:.2f}".format(mean_precision))

joblib.dump(model11, 'extra_trees_classifier_model.pkl')


mses = []
r2_scores = []
accuracies = []
precisions = []

model11 = xgb.XGBClassifier()

i = 1

# Train XGBoost Classifier
for train_index, test_index in tscv.split(X):
    print(i)
    i += 1
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    print(len(X_train))
    print(len(y_train))
    print(len(X_test))
    print(len(y_test))

    model11.fit(X_train, y_train)

    y_pred = model11.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mses.append(mse)

    r2 = r2_score(y_test, y_pred)
    r2_scores.append(r2)

    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)

    precision = precision_score(y_test, y_pred)
    precisions.append(precision)

mean_mse = sum(mses) / len(mses)
mean_r2 = sum(r2_scores) / len(r2_scores)
mean_accuracy = sum(accuracies) / len(accuracies)
mean_precision = sum(precisions) / len(precisions)
print('XGBoost model')
print("MSE: {:.2f}".format(mean_mse))
print("R-squared: {:.2f}".format(mean_r2))
print("Accuracy: {:.2f}%".format(mean_accuracy * 100))
print("Precision: {:.2f}".format(mean_precision))

joblib.dump(model11, 'xgboost_model_v2.pkl')


mses = []
r2_scores = []
accuracies = []
precisions = []

model3 = RandomForestClassifier()

i = 1

# Train Random Forest
for train_index, test_index in tscv.split(X):
    print(i)
    i += 1
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    print(len(X_train))
    print(len(y_train))
    print(len(X_test))
    print(len(y_test))

    model3.fit(X_train, y_train)

    y_pred = model3.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mses.append(mse)

    r2 = r2_score(y_test, y_pred)
    r2_scores.append(r2)

    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)

    precision = precision_score(y_test, y_pred)
    precisions.append(precision)

mean_mse = sum(mses) / len(mses)
mean_r2 = sum(r2_scores) / len(r2_scores)
mean_accuracy = sum(accuracies) / len(accuracies)
mean_precision = sum(precisions) / len(precisions)

print("MSE: {:.2f}".format(mean_mse))
print("R-squared: {:.2f}".format(mean_r2))
print("Accuracy: {:.2f}%".format(mean_accuracy * 100))
print("Precision: {:.2f}".format(mean_precision))

joblib.dump(model3, 'random_forest_model.pkl')
