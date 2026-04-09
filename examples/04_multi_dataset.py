"""Multi-dataset scenario with data processing.

Passes two DataFrames to NVEIL. The AI plans a join and aggregation,
then generates a comparison chart. All processing runs locally.
"""

import os
import nveil
import pandas as pd
import numpy as np

nveil.configure(
    api_key=os.environ["NVEIL_API_KEY"],
)

# ── Two separate datasets ──
actual_sales = pd.DataFrame({
    "region": np.random.choice(["North", "South", "East", "West"], 100),
    "revenue": np.random.uniform(10000, 60000, 100).round(2),
})

targets = pd.DataFrame({
    "region": ["North", "South", "East", "West"],
    "target": [45000, 35000, 40000, 50000],
})

print("Actual sales:")
print(actual_sales.groupby("region")["revenue"].mean().round(0))
print()
print("Targets:")
print(targets)
print()

# ── Generate: NVEIL joins the datasets and builds the chart ──
print("Generating spec (NVEIL will join and aggregate the data)...")
spec = nveil.generate_spec(
    "Compare average actual revenue vs target by region",
    {"actual_sales": actual_sales, "targets": targets},
)
print(f"Explanation: {spec.explanation}")

# ── Render and export ──
print("Rendering...")
fig = spec.render({"actual_sales": actual_sales, "targets": targets})

nveil.save_image(fig, "output/comparison.png")
print("Saved: output/comparison.png")

nveil.save_html(fig, "output/comparison.html")
print("Saved: output/comparison.html")

nveil.show(fig)
print("Done!")
