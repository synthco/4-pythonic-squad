# Alarms Prediction System

**How to Use**

We are developing a program which would be able to predict air alarms for 12 next hours for any region(“oblast”-“область”) in Ukraine. It would base it’s predictions on the historical data and forecasts from ISW(Institute for the Study of War), alarms APIs and Visual Crossing.
Make sure you have done (one of these) points to start it:
* create a SaaS system via AWS tools. 

*have your own key generated (use the link in weather_app.py)
*have a Postman installed (10.22.9 is recommended)
*have backend.py file on your jupyter notebook server (as all other files from Backend, ISW and Weather folders)
*connect to the file using the following command: uwsgi --http 0.0.0.0:8000 --wsgi-file backend.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191 command.
* insert the created token and key to the file backend.py
* install the requirments.txt file

To run:
* 1) Go to Postman
* 2) Choose "Create a new collection"
* 3) Choose method "Post"
* 4) Modify link: http://your-ip4:8000/predict
* 5) Choose "Body" and "row" types of request
* 6) create a postman request in format:
* {
* token: "token",
* locations : ["location1", "location2"..]
* }

To use Frontend part, another instance is required.
To run application on local server - use:
* cd "directory/with/frondent"
* "yarn dev" command
* insert link in any browser.

**Content**
* Evaluating and visual - evaluation and EDA for the model
* ML - model training
* NLP - NLP + vectorization for ISW.csv
* ISW - getter for ISW
* Backend/API - DFenfer for new data for prediction getter
* Backend/main_backend - file for the request


* Developed by: Tyschenko Ivan, Spitkovska Vladyslava, Zasyadko Matiy, Nych Kateryna, Honcharenko Vladyslav
