"""Subcommand modules for the ``nveil`` CLI.

Each module exposes:
    NAME           — the subcommand name (e.g. "generate")
    register(sp)   — attach the argparse subparser
    run(args) -> int  — execute the subcommand, return exit code
"""
