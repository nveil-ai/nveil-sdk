"""Basic chart generation from a DataFrame.

Generates a bar chart from sales data, displays it in the browser,
and saves it as PNG and HTML.
"""

import os
import nveil
import pandas as pd
import numpy as np

# ── Configure ──
nveil.configure(
    api_key=os.environ["NVEIL_API_KEY"],
)

# ── Create sample data ──
df = pd.DataFrame({
    "region": ["North", "South", "East", "West", "Central"],
    "revenue": [42000, 38000, 51000, 27000, 45000],
    "quarter": ["Q1", "Q1", "Q1", "Q1", "Q1"],
})

spec = nveil.generate_spec("Bar chart of revenue by region", df)
fig = spec.render(df)

nveil.save_image(fig, "output/basic_chart.png")
nveil.save_html(fig, "output/basic_chart.html")
nveil.show(fig)

