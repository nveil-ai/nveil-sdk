"""``nveil generate`` — create a spec from a prompt + data file."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from ..config import configure_from_args


NAME = "generate"
_VALID_FORMATS = ("html", "png", "nveil", "all")
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def register(subparsers) -> None:
    p = subparsers.add_parser(
        NAME,
        help="Generate a chart from a natural-language prompt and a data file.",
        description=(
            "Generate a visualization specification, render it, and write the "
            "resulting artifact(s) to disk. Paths of the created files are "
            "printed to stdout (one per line)."
        ),
    )
    p.add_argument("prompt", help="Natural-language description of the desired chart.")
    p.add_argument(
        "--data", required=True,
        help="Path to a CSV / Parquet / JSON / Excel file. No DataFrame load in this process.",
    )
    p.add_argument(
        "-o", "--output",
        help="Output path (extension inferred) or directory. Default: ./nveil_out/<slug>.<ext>",
    )
    p.add_argument(
        "-f", "--format", choices=_VALID_FORMATS, default="html",
        help="Output format. 'all' writes html + png + .nveil and prints the explanation.",
    )
    p.add_argument(
        "--explain", action="store_true",
        help="Print the spec's human-readable explanation to stdout.",
    )
    p.add_argument("--api-key", help="Override NVEIL_API_KEY for this invocation.")
    p.set_defaults(_run=run)


def _slug(text: str, max_len: int = 50) -> str:
    s = _SLUG_RE.sub("_", text.lower()).strip("_")
    return s[:max_len] or "chart"


def _resolve_output_paths(
    output: str | None, prompt: str, formats: tuple[str, ...],
) -> dict[str, Path]:
    """Return {fmt: Path} for each requested format."""
    if output:
        out = Path(output)
        if out.suffix and len(formats) == 1:
            # Explicit file path given — use it for the single format
            return {formats[0]: out}
        # Directory (or multi-format): fall through to stem-based naming
        base_dir = out if not out.suffix else out.parent
        stem = out.stem if out.suffix else _slug(prompt)
    else:
        base_dir = Path("nveil_out")
        stem = _slug(prompt)
    base_dir.mkdir(parents=True, exist_ok=True)
    return {fmt: base_dir / f"{stem}.{fmt}" for fmt in formats}


def run(args) -> int:
    configure_from_args(args)

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"nveil: error: data file not found: {data_path}", file=sys.stderr)
        return 1

    import nveil  # picks up freshly-configured client

    formats = ("html", "png", "nveil") if args.format == "all" else (args.format,)
    out_paths = _resolve_output_paths(args.output, args.prompt, formats)

    spec = nveil.generate_spec(args.prompt, data_path)

    # .nveil output can be written from spec alone; html/png need a render.
    if "nveil" in out_paths:
        spec.save(str(out_paths["nveil"]))
        print(str(out_paths["nveil"]))

    if any(f in out_paths for f in ("html", "png")):
        fig = spec.render(data_path)
        if "html" in out_paths:
            nveil.save_html(fig, str(out_paths["html"]))
            print(str(out_paths["html"]))
        if "png" in out_paths:
            nveil.save_image(fig, str(out_paths["png"]))
            print(str(out_paths["png"]))

    if args.explain or args.format == "all":
        print("---")
        print(spec.explanation)
    return 0
