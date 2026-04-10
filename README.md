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

The AI-for-data-viz space has moved fast. Here's how NVEIL compares to what's actually available in 2026.

| Capability | **NVEIL** | ChatGPT / Claude / Gemini<br>(data analysis modes) | PandasAI / LIDA / Julius<br>(LLM-to-viz OSS & SaaS) | Plotly / Matplotlib / Seaborn<br>(traditional libraries) |
|---|:-:|:-:|:-:|:-:|
| Natural-language input | ✓ | ✓ | ✓ | ✗ |
| Raw data never leaves your machine | ✓ | ✗ — uploaded to the provider | ✗ — LLM sees row samples | ✓ |
| Only schema + aggregate stats sent to server | ✓ | ✗ | ✗ | N/A |
| Deterministic, reproducible output | ✓ — constraint solver | ✗ — same prompt, different chart each run | ✗ — LLM variance | ✓ — you write the code |
| Offline re-rendering (zero API calls after first spec) | ✓ | ✗ | ✗ | ✓ |
| Portable saved specs — render forever on new data | ✓ `.nveil` files | ✗ | ✗ | ✗ |
| 2D + 3D + geospatial + scientific / medical imaging | ✓ single SDK | Mostly 2D (matplotlib sandbox) | Mostly 2D | Per-library, manual |
| Multi-backend auto-selected (Plotly, VTK, DeckGL) | ✓ | ✗ | ✗ | Single library per import |
| Full data-processing pipeline in the same call | ✓ joins, pivots, geocoding, time-series, features | ✓ (but non-deterministic) | Partial | ✗ (separate tooling) |
| Cost model | Metered per spec, render is free | Per-token / per-message | Per-token or subscription | Free / self-hosted |

**The short version:** Chatbot data-analysis modes upload your raw data to a third party and give different results every run. Open-source LLM-to-viz libraries still send data samples to the model and are non-deterministic. Traditional libraries are private and reproducible but require you to write every chart by hand. NVEIL is the only option that is **private** (schema-only), **deterministic** (constraint-solved specs), **offline-replayable** (render forever from a saved `.nveil` file), and **natural-language driven** — all in one SDK.

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
