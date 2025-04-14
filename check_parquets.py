import pandas as pd

# Replace with your actual file path
file_path = r"C:\Users\AMSHU\Downloads\dataset\test-00000-of-00001.parquet"

# Read the Parquet file
df = pd.read_parquet(file_path)

# Print the top 5 rows
print(df.head())  # List of all column names
