from dfender import Dfender
import subprocess
import pandas as pd
def test_dfender():
    dfender = Dfender()
    # df1 = dfender.isw_vector
    # df2 = dfender.weather_vector
    #
    # df1.to_csv("ISW.csv", index=False)
    # df2.to_csv("Weather.csv", index=False)
    df = dfender.vector
    df.to_csv('predict_vector.csv')
    print(dfender.result)

    # print(dfender)

if __name__ == '__main__':
    # Виконати команду pip для встановлення пакету xgboost
    subprocess.run(["pip", "install", "xgboost"])

    print("XGBoost successfully installed!")
    test_dfender()


