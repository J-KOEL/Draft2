import pandas as pd

def load_csv_dict(file_path, key_col=None, value_col=None):
    df = pd.read_csv(file_path)

    # Case 1: Nested dictionary for lens color files
    if set(['Code', 'Color', 'PartNumber']).issubset(df.columns):
        return {
            str(row['Code']).strip(): {
                "Color": str(row['Color']).strip(),
                "PartNumber": str(row['PartNumber']).strip()
            }
            for _, row in df.iterrows()
        }

    # Case 2: Explicit key-value columns provided
    if key_col and value_col:
        if key_col not in df.columns or value_col not in df.columns:
            raise ValueError(f"Expected columns '{key_col}' and '{value_col}' in {file_path}. Found: {df.columns.tolist()}")
        return {
            str(row[key_col]).strip(): str(row[value_col]).strip()
            for _, row in df.iterrows()
        }

    # Case 3: Default to 'Code' and 'Label' if they exist
    if 'Code' in df.columns and 'Label' in df.columns:
        return {
            str(row['Code']).strip(): str(row['Label']).strip()
            for _, row in df.iterrows()
        }

    # Case 4: Auto-detect if exactly two columns
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
