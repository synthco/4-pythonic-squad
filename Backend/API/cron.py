from Backend.API.dfender import Dfender
import pickle

dfender = Dfender()
prediction_array = dfender.result

with open('prediction_array.pkl', 'wb') as f:
    pickle.dump(prediction_array, f)
