import pandas as pd

def load_csv_dict(file_path, key_col="Code", value_col="Label"):
    df = pd.read_csv(file_path)
    return {str(row[key_col]).strip(): str(row[value_col]).strip() for _, row in df.iterrows()}

def load_alternate_map(file_path):
    df = pd.read_csv(file_path)
    return {str(row["Alternate"]).strip().upper(): str(row["Standard"]).strip().upper() for _, row in df.iterrows()}
