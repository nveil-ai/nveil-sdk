# NVEIL Python SDK

**Describe your data. Get production charts. Your data stays local.**

NVEIL is an AI-powered data visualization SDK. Write one line of natural language, and NVEIL processes your data and generates publication-ready visualizations — no chart code, no hallucinations, no data leaving your machine.

```python
import nveil
import pandas as pd

nveil.configure(api_key="nveil_...")

df = pd.read_csv("sales.csv")
spec = nveil.generate_spec("Revenue by region, colored by quarter", df)

fig = spec.render(df)       # 100% local — no API call
nveil.show(fig)              # opens in browser
```

## Why NVEIL?

| Feature | NVEIL | Plotly / Matplotlib | ChatGPT / Copilot |
|---------|-------|--------------------|--------------------|
| Natural language input | Yes | No | Yes |
| Deterministic output | Yes | N/A | No |
| Data stays local | Yes | Yes | No |
| Offline rendering | Yes | Yes | No |
| 50+ viz types (2D, 3D, geo, medical) | Yes | Manual | Unreliable |
| Reusable specs | Yes | No | No |

## How It Works

1. **You describe** what you want in plain language
2. **NVEIL AI plans** the data processing and visualization (only metadata is sent — column names, types, statistics)
3. **The SDK executes locally** — joins, aggregations, pivots, rendering — all on your machine
4. **You get a figure** — Plotly, VTK, or DeckGL, auto-selected for your data

```
Your Data → SDK (metadata only) → NVEIL AI → Processing Plan → Local Execution → Result
              ↑                                                        ↑
         raw data stays here                                    raw data stays here
```

## Key Features

- **Two engines in one** — data processing (joins, pivots, aggregations, geocoding, time series) AND visualization generation from a single prompt
- **Auditable results** — powered by constraint solving, not random generation. Same input = same output, every time
- **Data privacy by design** — raw data never leaves your machine. Only column names, types, and aggregate statistics are sent
- **Offline rendering** — `spec.render()` runs 100% locally with zero API calls
- **Reusable specs** — save to `.nveil` files, reload later, render on new data without a server
- **Multi-backend** — auto-detects the best engine: Plotly (2D charts), VTK (3D/medical), DeckGL (geospatial)

## Save Once, Render Forever

```python
# Generate once (API call)
spec = nveil.generate_spec("Monthly trend by category", df)
spec.save("trend.nveil")

# Reload anywhere — no API call, no server, no cost
spec = nveil.load_spec("trend.nveil")
fig = spec.render(fresh_data)
nveil.save_image(fig, "report.png")
```

## Getting Started

```bash
pip install nveil
```

1. Create an account at [app.nveil.com](https://app.nveil.com)
2. Generate an API key in **Settings**
3. Start visualizing

Full documentation: [docs.nveil.com](https://docs.nveil.com)

## License

Proprietary. See [LICENSE](LICENSE) for details.
