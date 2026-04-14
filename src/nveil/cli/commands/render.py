"""``nveil render`` — re-render a saved .nveil spec against fresh data."""

from __future__ import annotations

import sys
from pathlib import Path

from ..config import configure_from_args
from .generate import _VALID_FORMATS, _resolve_output_paths, _slug


NAME = "render"


def register(subparsers) -> None:
    p = subparsers.add_parser(
        NAME,
        help="Re-render a saved .nveil spec against a data file (no API call).",
        description=(
            "Load an opaque .nveil spec and render it locally. This is free — "
            "no server round trip."
        ),
    )
    p.add_argument("spec", help="Path to a .nveil file.")
    p.add_argument("--data", required=True, help="Path to a compatible data file.")
    p.add_argument(
        "-o", "--output",
        help="Output path or directory. Default: ./nveil_out/<spec-stem>.<ext>",
    )
    p.add_argument(
        "-f", "--format", choices=_VALID_FORMATS, default="html",
        help="Output format. 'all' writes html + png.",
    )
    p.add_argument("--api-key", help="Unused for offline render; accepted for symmetry.")
    p.set_defaults(_run=run)


def run(args) -> int:
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"nveil: error: spec file not found: {spec_path}", file=sys.stderr)
        return 1
    data_path = Path(args.data)
    if not data_path.exists():
        print(f"nveil: error: data file not found: {data_path}", file=sys.stderr)
        return 1

    # render doesn't call the API, but nveil.load_spec + nveil.save_image need
    # the package loaded. Configure lazily so missing API key is not fatal here.
    try:
        configure_from_args(args)
    except Exception:
        pass

    import nveil

    spec = nveil.load_spec(str(spec_path))
    formats = ("html", "png") if args.format == "all" else (args.format,)
    # "nveil" format is a no-op on render (the file is already the spec itself).
    formats = tuple(f for f in formats if f != "nveil")

    out_paths = _resolve_output_paths(args.output, spec_path.stem, formats)
    fig = spec.render(data_path)
    if "html" in out_paths:
        nveil.save_html(fig, str(out_paths["html"]))
        print(str(out_paths["html"]))
    if "png" in out_paths:
        nveil.save_image(fig, str(out_paths["png"]))
        print(str(out_paths["png"]))
    return 0
