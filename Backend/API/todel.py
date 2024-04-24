import joblib
import pandas as pd
with open("/Users/ivantyshchenko/Documents/GitHub/4-pythonic-squad/Backend/API/XGBoost_model.pkl", 'rb+') as f:
    try:
        xgboost = joblib.load(f)
        print('Done!')
    except FileNotFoundError:
        print("XGBoost model file not found.")

booster = xgboost.get_booster()
feature_names = booster.feature_names
# print(feature_names)

df = pd.read_csv("predict_vector.csv")

column_names = set(df.columns)

# Compare feature names with DataFrame column names
common_names = set(feature_names).difference(column_names)

# Print the common names
print("Different names between XGBoost feature names and DataFrame columns:")
print(common_names)


