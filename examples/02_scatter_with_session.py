"""Session-based workflow with multiple chart types.

Uses a session to generate a scatter plot and a line chart from
the same data. The data pipeline runs once and is reused.
"""

import os
import nveil
import pandas as pd
import numpy as np

nveil.configure(
    api_key=os.environ["NVEIL_API_KEY"],
)

# ── Larger dataset ──
np.random.seed(42)
df = pd.DataFrame({
    "region": np.random.choice(["North", "South", "East", "West"], 200),
    "revenue": np.random.uniform(5000, 80000, 200).round(2),
    "units_sold": np.random.randint(10, 500, 200),
    "margin": np.random.uniform(0.05, 0.45, 200).round(3),
    "quarter": np.random.choice(["Q1", "Q2", "Q3", "Q4"], 200),
})
print(f"Data: {df.shape[0]} rows, {df.shape[1]} columns")
print(df.describe().round(2))
print()

# ── Session: generate multiple specs, pipeline runs once ──
with nveil.session() as s:
    print("Generating scatter plot...")
    scatter_spec = s.generate_spec("Scatter plot of revenue vs margin, colored by region", df)
    print(f"  {scatter_spec.explanation}")

    print("Generating line chart...")
    line_spec = s.generate_spec("Average revenue by quarter, one line per region", df)
    print(f"  {line_spec.explanation}")

    print("Rendering scatter...")
    fig_scatter = scatter_spec.render(df)
    nveil.save_image(fig_scatter, "output/scatter.png")
    print("  Saved: output/scatter.png")

    print("Rendering line...")
    fig_line = line_spec.render(df)
    nveil.save_image(fig_line, "output/line_chart.png")
    print("  Saved: output/line_chart.png")

    print()
    print(s.timer.summary())

print("Done!")
