import pickle

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

from model.Input_model import TrainInput, PredictionInput

categorical_columns = ['district', 'construction_status', 'market']


def train(data_to_train: TrainInput, path_to_csv: str, path_to_model: str) -> None:
    """Train a RandomForestRegressor model and save it to a file."""
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
    with open(path_to_model, 'wb') as f:
        pickle.dump(model_data, f)


def predict(model_file: str, input_data: PredictionInput) -> float:
    """Load a trained model from a file and make a prediction."""
    with open(model_file, 'rb') as f:
        model_data = pickle.load(f)

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


def calculate_floor_ratio(floor: int, total_floors: int) -> float:
    """Calculate the floor ratio."""
    if total_floors == 0:
        return 0.0
    return floor / total_floors


def encode_categorical_columns_with_encoders(df: pd.DataFrame, cols: list):
    """Encode categorical columns using LabelEncoder and return the encoders."""
    encoders = {}
    df_copy = df.copy()

    for col in cols:
        le = LabelEncoder()
        df_copy[col] = le.fit_transform(df_copy[col])
        encoders[col] = le

    return df_copy, encoders


def apply_encoders(df: pd.DataFrame, encoders: dict, cols: list) -> pd.DataFrame:
    """Apply the provided encoders to the specified columns in the DataFrame."""
    df_copy = df.copy()

    for col in cols:
        if col in encoders:
            df_copy[col] = encoders[col].transform(df_copy[col])

    return df_copy