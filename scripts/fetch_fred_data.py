import os
from dotenv import load_dotenv
from fredapi import Fred
import pandas as pd

# Load the API key from .env
load_dotenv()
fred_key = os.getenv("FRED_API_KEY")
fred = Fred(api_key=fred_key)

# Pick a test series — Industrial Production Index
series_id = "INDPRO"
data = fred.get_series(series_id)

# Convert to DataFrame
df = pd.DataFrame(data)
df.columns = ['value']
df.index.name = 'date'

# Preview
print(df.tail())
