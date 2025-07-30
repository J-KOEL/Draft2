import pandas as pd

def load_csv_dict(file_path, key_col="Code", value_col=None):
    df = pd.read_csv(file_path)

    # If value_col is provided, return a simple key-value dictionary
    if value_col:
        return {
            str(row[key_col]).strip(): str(row[value_col]).strip()
            for _, row in df.iterrows()
        }

    # If no value_col is provided, return a nested dictionary (e.g., for lens color)
    elif set(['Code', 'Color', 'PartNumber']).issubset(df.columns):
        return {
            str(row['Code']).strip(): {
                "Color": str(row['Color']).strip(),
                "PartNumber": str(row['PartNumber']).strip()
            }
            for _, row in df.iterrows()
        }

    else:
        raise ValueError(f"Unexpected format in {file_path}. Please check column names.")

def load_alternate_map(file_path):
    df = pd.read_csv(file_path)
    return {
        str(row["Alternate"]).strip().upper(): str(row["Standard"]).strip().upper()
        for _, row in df.iterrows()
    }
