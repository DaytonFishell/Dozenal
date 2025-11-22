# Dozenal Project Instructions for AI Agents

## What to know up front
- This project is a single small package under `src/dozenal/`. The only implemented module today is `dozenal_decimal_converter.py`, so treat that file as the definitive logic source for base-12 conversions.
- The package entry point (`src/dozenal/__init__.py`) exposes `main()` that prints a placeholder message; new CLI behavior must be wired through the `dozenal = dozenal:main` script declared in `pyproject.toml`.
- Python 3.14+ is required (`pyproject.toml` and `.python-version`), and the repo bootstraps via `uv_build` (see `pyproject.toml`).

## Key patterns to follow
- `_DOZENAL_DIGITS = "0123456789TE"` defines the mapping. All digit validation and formatting logic should index this string so updates in one place affect both serialization and parsing.
- `decimal_to_dozenal` distinguishes ints, floats, and `Decimal` inputs. Floats are first converted to `Fraction(...).limit_denominator(10**9)`, wrapped in `Decimal`, and then split into integer and fractional parts. When expanding new behavior, mirror that flow to preserve exactness for repeating base-12 fractions.
- `_int_to_base12` and `_int_from_base12` handle sign-less integer parts without lookup caches; keep their loops straightforward when extending integer logic.
- `dozenal_to_decimal` uppercases and strips whitespace before splitting on `.`; extra decimal points or invalid characters raise `ValueError`. Fractional digits are accumulated by dividing by successive powers of 12 so new parsing logic (e.g., suffixes) must keep that Decimal accumulation strategy.
- Tests in `tests/test_dozenal_decimal_converter.py` rely on the helper in `tests/conftest.py` to inject `src` into `sys.path`. Any new tests should live under `tests/` and keep the same pytest style (parameterized cases) so they run predictably.
- The `if __name__ == "__main__"` block in `dozenal_decimal_converter.py` is a simple CLI for quick conversions; more complex CLI features should be added to `src/dozenal/cli.py` and routed through the main entry point.
- When adding new tools, create separate modules under `src/dozenal/` and add them to the `_TOOLS` mapping in `cli.py` for automatic CLI integration.
- The CLI uses `argparse` for parsing; maintain the existing structure when adding new flags or tools to ensure consistent user experience.
- This project uses strict type hints and `mypy` for static analysis. When adding new functions or modules, ensure all public APIs are fully annotated and that `mypy` checks pass without errors.

## Workflow nuggets
- Run the unit suite with `python -m pytest tests`. (There is no custom runner defined yet, so helper scripts or `uv` commands are unnecessary.)
- Build or package the project with `uv build` from the repo root because the build backend is `uv_build` and the lockfile is `uv.lock`.
- The CLI script named `dozenal` maps to `dozenal:main`; command routing now lives in `src/dozenal/cli.py` and exposes a `--tool/-t` flag with a converter tool that mirrors the standalone converter CLI.

## CLI guidance
- The `dozenal` CLI runs `run_cli` in `src/dozenal/cli.py`, which lists available tools and currently defaults to the `converter` tool backed by `src/dozenal/dozenal_decimal_converter.py`.
- Use the converter via `dozenal --tool converter --to-doz 3.5` or `dozenal --tool converter --to-dec T`. The CLI enforces at least one of `--to-doz`/`--to-dec` when converter is selected and accepts `--frac-precision` for fractional conversion.
- `--list-tools` enumerates future tools and integrates easily with new command files once they are added to `_TOOLS`.

## When editing conversions or adding features
- Preserve the `Decimal` context precision logic (`getcontext().prec = max(28, frac_precision * 3)`) before computing fractional digits; it ensures repeated multiplications stay accurate.
- Negative values are handled by keeping track of a `sign` string and applying it after the conversion loops, so maintain that separation when adding new branches.
- When introducing more digits or alternative representations (e.g., lowercase output), update both `_DOZENAL_DIGITS` and `dozenal_to_decimal` validation loops together.
- Keep the CLI-friendly comment block in `dozenal_decimal_converter.py` (guarded by `if __name__ == "__main__"`) minimal; longer CLI features should live in separate modules to avoid inflating the conversion logic.

## Notes for future enhancements
- There are currently no async APIs or webhooks; focus on keeping conversions synchronous, deterministic, and easy to test.
- Use `Decimal` for any fractional computation even if the input is a float: that is the established precision pattern.
- No external dependencies beyond the standard library are declared, so avoid adding new packages unless necessary and, when you do, update `pyproject.toml` and regenerate `uv.lock` with `uv sync`.

Let me know if any sections above need clarification or if you want me to document additional workflows.