from sklearn.ensemble import RandomForestRegressor
import pickle

from model.PredictionInput import PredictionInput
from model.TrainInput import TrainInput
import pandas as pd
from sklearn.preprocessing import LabelEncoder


categorical_columns = ['district', 'construction_status', 'market']

"""Train the model with new data and save the updated model."""
def train(data_to_train: TrainInput, path_to_csv, path_to_model):

    df = pd.read_csv(path_to_csv)

    data = data_to_train.model_dump()

    calculated_floor_ratio = calculate_floor_ratio(data["floor"], data["total_floors"])

    new_row = [
        data["district"],
        data["price"],
        data["surface"],
        data["rooms_num"],
        data["construction_status"],
        data["market"],
        data["build_year"],
        data["transit_dur_s"],
        calculated_floor_ratio
    ]
    df.loc[len(df.index)] = new_row

    df_encoded, encoders = encode_categorical_columns_with_encoders(df.copy(), categorical_columns)

    df.to_csv(path_to_csv, index=False)

    x = df_encoded.drop("price", axis=1)
    y = df_encoded["price"]

    forest = RandomForestRegressor(n_estimators=10, random_state=2)
    forest.fit(x, y)

    model_data = {
        'model': forest,
        'encoders': encoders
    }
    pickle.dump(model_data, open(path_to_model, 'wb'))

def predict(model_file, input_data: PredictionInput) -> float:
    model_data = pickle.load(open(model_file, 'rb'))

    model = model_data['model']
    data = input_data.model_dump()
    encoders = model_data['encoders']


    calculated_floor_ratio = calculate_floor_ratio(data["floor"], data["total_floors"])

    input_df = pd.DataFrame([[
        data["district"],
        data["surface"],
        data["rooms_num"],
        data["construction_status"],
        data["market"],
        data["build_year"],
        data["transit_dur_s"],
        calculated_floor_ratio
    ]], columns=[
        'district',
        'surface',
        'rooms_num',
        'construction_status',
        'market',
        'build_year',
        'transit_dur_s',
        'floor_ratio'
    ])

    input_df = apply_encoders(input_df, encoders, categorical_columns)

    prediction = model.predict(input_df)

    return float(prediction[0])


"""Calculate the ratio of the floor number to the total number of floors in a building."""
def calculate_floor_ratio(floor: int, total_floors: int) -> float:
    if total_floors == 0:
        return 0.0
    return floor / total_floors

"""
Encode categorical columns using LabelEncoder and return the encoders for future use.
"""
def encode_categorical_columns_with_encoders(df: pd.DataFrame, categorical_columns: list):
    encoders = {}
    df_copy = df.copy()
    
    for col in categorical_columns:
        le = LabelEncoder()
        df_copy[col] = le.fit_transform(df_copy[col])
        encoders[col] = le  # Zapisz encoder
    
    return df_copy, encoders

"""Apply saved encoders to the input DataFrame."""
def apply_encoders(df: pd.DataFrame, encoders: dict, categorical_columns: list) -> pd.DataFrame:
    df_copy = df.copy()
    
    for col in categorical_columns:
        if col in encoders:
            df_copy[col] = encoders[col].transform(df_copy[col])
    
    return df_copy