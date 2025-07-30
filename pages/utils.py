import pandas as pd

def load_csv_dict(file_path, key_col="Code", value_col=None):
    df = pd.read_csv(file_path)

    # Nested dictionary for lens color files
    if set(['Code', 'Color', 'PartNumber']).issubset(df.columns):
        return {
            str(row['Code']).strip(): {
                "Color": str(row['Color']).strip(),
                "PartNumber": str(row['PartNumber']).strip()
            }
            for _, row in df.iterrows()
        }

    # If value_col is explicitly provided
    if value_col:
        if key_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"Expected columns '{key_col}' and '{value_col}' in {file_path}. Found: {df.columns.tolist()}")
        return {
            str(row[key_col]).strip(): str(row[value_col]).strip()
            for _, row in df.iterrows()
        }

    # If value_col is not provided, try to infer it
    if len(df.columns) == 2:
        key_col, value_col = df.columns
        return {
            str(row[key_col]).strip(): str(row[value_col]).strip()
            for _, row in df.iterrows()
        }

    raise ValueError(f"Unexpected format in {file_path}. Columns found: {df.columns.tolist()}")

def load_alternate_map(file_path):
    df = pd.read_csv(file_path)
    return {
        str(row["Alternate"]).strip().upper(): str(row["Standard"]).strip().upper()
        for _, row in df.iterrows()
    }
