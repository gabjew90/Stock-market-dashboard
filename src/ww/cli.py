"""`ww` command-line interface."""
from __future__ import annotations

import typer

app = typer.Typer(help="Wishing Wealth Wiki tooling.", no_args_is_help=True)


@app.callback()
def _main() -> None:
    """Wishing Wealth Wiki tooling."""


if __name__ == "__main__":  # pragma: no cover
    app()
