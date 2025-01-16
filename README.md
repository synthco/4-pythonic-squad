# Alarms Prediction System (Secure Sky)

## Overview

The Alarms Prediction System is designed to forecast air alarms for the next 12 hours across various regions ("oblasts") in Ukraine. Utilizing historical data and forecasts from the Institute for the Study of War (ISW), alarm APIs, and Visual Crossing, the system employs an XGBoost model to generate predictions.

## Prerequisites

To set up and run the application, ensure the following:

- **API Key**: Obtain a personal API key as specified in the `weather_app.py` file.

- **Postman**: Install Postman for API testing (version 10.22.9 is recommended).

- **Backend Files**: Ensure `backend.py` and all related files from the `Backend`, `ISW`, and `Weather` directories are present on your Jupyter Notebook server.

- **uWSGI**: Install uWSGI to serve the application.

- **Python Environment**: Install the required dependencies using the `requirements.txt` file.

## Setup Instructions

1. **Insert API Key**: Add your API key and token into the `backend.py` file at the designated locations.

2. **Start the Application**: Execute the following command to run the application:

   ```bash
   uwsgi --http 0.0.0.0:8000 --wsgi-file backend.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191

> [!IMPORTANT]
> make sure you've installed `requirments.py` in advance

- Reports and final deployment presentation: https://drive.google.com/drive/folders/1wVH3V8-xe_UUSB-20XnVCh1CyjxzpmpY?usp=sharing. 
- Developed by: Tyschenko Ivan, Spitkovska Vladyslava, Zasyadko Matiy, Nych Kateryna, Honcharenko Vladyslav
This enhanced README provides a clear and structured guide for understanding, setting up, and utilizing the Alarms Prediction System. Let us know if you need further assistance or additional information!
:: [Spitkopvska Vladyslava](https://github.com/tsaebst) , [Tyschenko Ivan](https://github.com/synthco)
