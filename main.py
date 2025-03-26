import pandas as pd
import numpy as np

print("✅ Python is working!")
print("📦 pandas version:", pd.__version__)
print("📦 numpy version:", np.__version__)

# Quick test: create a small DataFrame
df = pd.DataFrame({
    "A": np.random.randn(5),
    "B": np.random.rand(5),
})

print("\n📊 Sample DataFrame:")
print(df)
