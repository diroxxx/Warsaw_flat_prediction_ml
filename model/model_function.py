import pickle
import pandas as pd

from model.input_model import PredictionInput

categorical_columns = ['district', 'construction_status', 'market']

def predict(model_file: str, input_data: PredictionInput) -> float:
    """Load a trained model from a file and make a prediction."""
    with open(model_file, 'rb') as f:
        model_data = pickle.load(f)

    model = model_data['flat_model']
    data = input_data.model_dump()
    encoders = model_data['encoders']

    input_df = pd.DataFrame([{
        "district": data["district"],
        "surface": data["surface"],
        "rooms_num": data["rooms_num"],
        "floor_no": data["floor_no"],
        "building_floors_num": data["building_floors_num"],
        "construction_status": data["construction_status"],
        "market": data["market"],
        "build_year": data["build_year"],
        "transit_dur_s": data["transit_dur_s"],
    }])

    input_df = apply_encoders(input_df, encoders, categorical_columns)

    prediction = model.predict(input_df)

    return float(prediction[0])


def apply_encoders(df: pd.DataFrame, encoders: dict, cols: list) -> pd.DataFrame:
    """Apply the provided encoders to the specified columns in the DataFrame."""
    df_copy = df.copy()

    for col in cols:
        if col not in df_copy.columns:
            continue
        if col not in encoders:
            continue

    for col in cols:
        if col in encoders:
            df_copy[col] = encoders[col].transform(df_copy[col])

    return df_copy