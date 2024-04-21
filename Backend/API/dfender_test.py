from dfender import Dfender

def test_dfender():
    dfender = Dfender()
    # df1 = dfender.isw_vector
    # df2 = dfender.weather_vector
    #
    # df1.to_csv("ISW.csv", index=False)
    # df2.to_csv("Weather.csv", index=False)
    print(dfender.result)

    # print(dfender)

if __name__ == '__main__':
    test_dfender()
