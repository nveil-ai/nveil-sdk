"""NveilSpec — opaque visualization specification with local rendering.

Once generated, a spec can be reused unlimited times on new data with
compatible columns — no API call, no cost.

All internal processing is handled by the compiled engine. The SDK
only stores and passes opaque byte blobs.
"""

from __future__ import annotations

from typing import Any


class NveilSpec:
    """Opaque visualization specification with local rendering.

    Once generated, ``spec.render(new_data)`` is 100% local — no API call,
    no cost. Reusable on any data with compatible columns.
    """

    def __init__(self, spec_blob: bytes):
        self._blob = spec_blob
        self._session = None  # set by Session.generate_spec for workspace reuse

    def render(self, data: Any = None) -> Any:
        """Render using the auto-detected best backend (Plotly, VTK, DeckGL).

        100% local execution — no API call.

        If called within a session context (``with nveil.session()``),
        reuses the session's already-computed pipeline outputs —
        no pipeline re-run.

        Args:
            data: pandas DataFrame, dict of DataFrames, numpy array, or list.

        Returns:
            Backend-specific figure object (plotly.graph_objects.Figure, etc.)
        """
        from dive._engine import render as engine_render
        from .timing import Timer

        session = self._session
        timer = session.timer if session else Timer()

        pipeline_instance = None
        if session and session._pipeline:
            pipeline_instance = session._pipeline

        with timer.measure("render"):
            return engine_render(
                spec_blob=self._blob,
                data=data,
                choregraph_instance=pipeline_instance,
            )

    @property
    def explanation(self) -> str:
        """Human-readable description of what was generated."""
        from dive._engine import get_explanation
        return get_explanation(self._blob)

    def save(self, path: str) -> None:
        """Save to opaque .nveil file (encrypted binary)."""
        from dive._engine import save_spec
        save_spec(self._blob, path)

    @staticmethod
    def load(path: str) -> NveilSpec:
        """Load from opaque .nveil file."""
        from dive._engine import load_spec
        blob = load_spec(path)
        return NveilSpec(spec_blob=blob)


# ── Module-level display/export functions ──


def show(fig: Any, theme: str = "dark") -> None:
    """Display a figure in the default browser.

    Args:
        fig: Figure object returned by ``NveilSpec.render()``.
        theme: Display theme ("dark" or "light").
    """
    if fig is None:
        raise RuntimeError("No figure to display")

    import tempfile
    import webbrowser
    from dive.builder.export import export_image

    html = export_image(fig, extension="html", theme=theme)

    tmp = tempfile.NamedTemporaryFile(
        suffix=".html", delete=False, mode="w", encoding="utf-8",
    )
    tmp.write(html)
    tmp.close()
    webbrowser.open(f"file://{tmp.name}")


def save_image(
    fig: Any,
    path: str,
    theme: str = "dark",
    width: int = 1200,
    height: int = 800,
    scale: int = 1,
) -> None:
    """Save a figure as a static image.

    Format is inferred from the file extension.
    Supported: .png, .jpg, .svg, .pdf (require kaleido), .html

    Args:
        fig: Figure object returned by ``NveilSpec.render()``.
        path: Output file path (e.g. ``"chart.png"``).
        theme: Export theme ("dark" or "light").
        width: Image width in pixels.
        height: Image height in pixels.
        scale: Font/margin scale factor.
    """
    if fig is None:
        raise RuntimeError("No figure to export")

    from dive.builder.export import export_to_file

    try:
        export_to_file(fig, path, theme=theme, width=width, height=height, scale=scale)
    except RuntimeError as e:
        if "Chrome" in str(e) or "kaleido" in str(e).lower():
            # Auto-install Chrome for kaleido and retry
            import logging
            log = logging.getLogger("nveil")
            log.info("Installing Chromium for static image export (one-time setup)...")
            try:
                import kaleido
                kaleido.get_chrome_sync()
                export_to_file(fig, path, theme=theme, width=width, height=height, scale=scale)
            except Exception as install_err:
                raise RuntimeError(
                    "Static image export requires Chromium. Auto-install failed.\n"
                    "Run manually: python -c \"import kaleido; kaleido.get_chrome_sync()\"\n"
                    "Or save as HTML instead: nveil.save_html(fig, 'chart.html')"
                ) from install_err
        else:
            raise


def save_html(fig: Any, path: str, theme: str = "dark") -> None:
    """Save a figure as an interactive HTML file.

    Args:
        fig: Figure object returned by ``NveilSpec.render()``.
        path: Output file path (e.g. ``"chart.html"``).
        theme: Export theme ("dark" or "light").
    """
    from dive.builder.export import export_to_file
    export_to_file(fig, path, theme=theme)
