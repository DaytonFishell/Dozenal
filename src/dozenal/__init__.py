from collections.abc import Sequence

from .cli import run_cli


def main(argv: Sequence[str] | None = None) -> None:
    """Entrypoint that routes to the requested dozenal tool."""
    raise SystemExit(run_cli(argv))
