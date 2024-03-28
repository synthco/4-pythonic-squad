import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit

param_grid = [
    {
        'penalty': ['l1', 'l2'],
        'C': np.logspace(-4, 4, 8),
        'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
        'class_weight': [None, 'balanced'],
        'random_state': [None, 42],
        'tol': [1e-4, 1e-3, 1e-2],
        'dual': [False],
        'fit_intercept': [True, False],
    }
]

# clf = LogisticRegression(max_iter=30000) 98.19
# clf = LogisticRegression(max_iter=30000, solver='lbfgs') 98.19
# clf = LogisticRegression(max_iter=30000, solver='lbfgs', penalty='l2') #98.19
# clf = LogisticRegression(max_iter=50000, tol=0.001) 98.01
# clf = LogisticRegression(max_iter=50000, solver='newton-cg') 98.16
# clf = LogisticRegression(max_iter=50000, class_weight='balanced') 98.47%
# clf = LogisticRegression(max_iter=50000, class_weight='balanced', dual=False) 98.47
# clf = LogisticRegression(max_iter=50000, class_weight='balanced', random_state=42) 98.47
# clf = LogisticRegression(max_iter=50000, class_weight='balanced', fit_intercept=True) 98.47
# clf = LogisticRegression(max_iter=50000, class_weight='balanced', fit_intercept=False) 98.45
# clf = LogisticRegression(max_iter=50000, class_weight='balanced', solver='liblinear') 98.34
# clf = LogisticRegression(max_iter=50000, class_weight='balanced', solver='sag') 87.01
# clf = LogisticRegression(max_iter=50000, class_weight='balanced', C=np.logspace(-4, 4, 2)[1]) 98.95
# clf = LogisticRegression(max_iter=50000, class_weight='balanced', solver='newton-cg', C=np.logspace(-4, 4, 2)[1],
                                                                                              # penalty='l2') 99.36
# random_state не впливає dual не впливає
# clf = LogisticRegression(max_iter=50000, class_weight='balanced', solver='newton-cg', C=np.logspace(-4, 4, 2)[1],
                                                                                # penalty='l2', tol=0.000001) 99.45
clf = LogisticRegression(max_iter=50000, class_weight='balanced', solver='newton-cg', C=np.logspace(-4, 4, 2)[1], penalty='l2', tol=0.000001)

data = pd.read_csv('/Users/matvejzasadko/Downloads/All/Python_cource_project/4-pythonic-squad/source/final_dataset.csv',
                   nrows=30000)
data = data.drop(['date', 'hour_datetime'], axis=1)

X = data.drop('is_alarm', axis=1)
y = data['is_alarm']

tscv = TimeSeriesSplit(n_splits=5)
print(tscv)
accuracies = []

i = 1
# Train LogisticRegression
for train_index, test_index in tscv.split(X):
    print(i)
    i += 1
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    print(len(X_train))
    print(len(y_train))
    print(len(X_test))
    print(len(y_test))

    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)
    accuracies.append(accuracy)


#print(clf.best_estimator_)

mean_accuracy = sum(accuracies) / len(accuracies)
print("Середня точність моделі: {:.2f}%".format(mean_accuracy * 100))

#joblib.dump(clf, 'logistic_regression_model_hp.pkl')

