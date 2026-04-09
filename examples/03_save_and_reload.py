"""Save a spec and reload it later for offline rendering.

Demonstrates the full lifecycle: generate once, save to .nveil,
reload on a different dataset, render without any server call.
"""

import nveil
import pandas as pd
import numpy as np
import os

nveil.configure(
    api_key=os.environ["NVEIL_API_KEY"],
)

# ── Generate spec from 2024 data ──
df_2024 = pd.DataFrame({
    "month": pd.date_range("2024-01-01", periods=12, freq="MS"),
    "revenue": [30, 32, 35, 40, 42, 45, 43, 47, 50, 48, 52, 55],
    "costs": [20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32],
})
df_2024["revenue"] *= 1000
df_2024["costs"] *= 1000

print("Step 1: Generate spec from 2024 data")
spec = nveil.generate_spec("Revenue and costs over time as a line chart", df_2024)
print(f"  Explanation: {spec.explanation}")

# ── Save ──
spec.save("output/monthly_trend.nveil")
file_size = os.path.getsize("output/monthly_trend.nveil")
print(f"  Saved: output/monthly_trend.nveil ({file_size} bytes)")

# ── Simulate loading later, on new data ──
print()
print("Step 2: Reload spec (no server call)")
loaded_spec = nveil.load_spec("output/monthly_trend.nveil")
print(f"  Explanation: {loaded_spec.explanation}")

# ── Render on 2025 data ──
df_2025 = pd.DataFrame({
    "month": pd.date_range("2025-01-01", periods=6, freq="MS"),
    "revenue": [58, 61, 64, 68, 72, 75],
    "costs": [33, 34, 35, 36, 37, 38],
})
df_2025["revenue"] *= 1000
df_2025["costs"] *= 1000

print()
print("Step 3: Render on 2025 data (offline, no server)")
fig = loaded_spec.render(df_2025)
nveil.save_image(fig, "output/trend_2025.png")
print("  Saved: output/trend_2025.png")

nveil.save_html(fig, "output/trend_2025.html")
print("  Saved: output/trend_2025.html")

print()
print("Done! The spec was generated once and reused on new data.")
