# Warsaw flat prediction API

A machine learning application for predicting apartment prices in Warsaw.  The project consists of a FastAPI backend and a Streamlit web interface.

## Contents
- \`Project description\`
- \`Training data information\`
- \`Installation\`
- \`Usage\`

## Project description
This application uses a machine learning model to predict apartment prices in Warsaw based on various features such as location, surface area, year of construction, and other property characteristics. 

## Training data information
The training data consists of a CSV file named \`warsaw_flats.csv\`, which contains the following columns:
- \`area\`: The area of the flat in square meters.
- \`num_rooms\`: The number of rooms in the flat.
- \`location\`: The location of the flat within Warsaw.
- \`floor\`: The floor number of the flat.
- \`year_built\`: The year the building was constructed.
- \`price\`: The price of the flat in PLN (target variable).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/diroxxx/Warsaw_flat_prediction_ml.git
    cd Warsaw_flat_prediction_ml
    ```
2. Create a virtual environment and activate it: 
   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage
1. Start the FastAPI server using Uvicorn:
   ```bash
   python  ./api.py
   ```
2. Access the API documentation at \`http://127.0.0.1:8008/docs \` to explore the available endpoints and test the API.
3. Use the \`/predict\` endpoint to make predictions by sending a POST request with the required features in the request body.
4. Use the \`/train\` endpoint to retrain the model with new data if needed.
5. To stop the server, press \`CTRL + C\` in the terminal where the server is running.
## Example Request 
Here is an example of a JSON payload to send to the \`/predict\` endpoint:
```json
{
  "district": "Mokotów",
  "surface": 60.5,
  "rooms_num": 3,
  "construction_status": "do zamieszkania",
  "market": "wtórny",
  "build_year": 2005,
  "floor": 2,
  "total_floors": 5,
  "transit_dur_s": 1200
}
```

## Example Response
The response from the \`/predict\` endpoint will be a JSON object containing the predicted price:
```json
{
  "predicted_price": 550000.0
}
```
  
   
