# Dozenal Project Instructions for AI Agents

## What to know up front
- The package lives entirely under `src/dozenal/` with two feature modules today: `dozenal_decimal_converter.py` (base-12 conversion utilities) and the new `dozenal_calc.py` (expression calculator). `src/dozenal/cli.py` wires both together behind the `dozenal` entry point declared as `dozenal = dozenal:main` in `pyproject.toml`.
- `src/dozenal/__init__.py` now delegates directly to `run_cli`, so any CLI changes must stay inside `cli.py` and new tool modules registered in `_TOOLS`.
- Python 3.14+ is required (`pyproject.toml`/`.python-version`), and the project builds with `uv_build`; keep that backend in mind when updating dependencies or packaging.

## Key patterns to follow
- `_DOZENAL_DIGITS = "0123456789TE"` remains the single source of truth for parsing/formatting dozenal digits. Reference it (or the derived `_ALLOWED_DIGITS` set in `dozenal_calc.py`) in any new parsing logic so all modules stay consistent.
- `decimal_to_dozenal` normalizes ints, floats, and `Decimal`s by routing floats through `Fraction(...).limit_denominator(10**9)` before switching to `Decimal`, then splits integer/fractional parts to multiply the fractional remainder by 12 repeatedly. Match that flow when adding new features touching fractional conversion precision.
- `_int_to_base12`/`_int_from_base12` keep the integer loop simple and sign-less. Any extensions that accept signed inputs should wrap these helpers rather than changing their inner loops.
- `dozenal_to_decimal` uppercases, trims, and validates digits before accumulating fractional digits via successive powers of 12 so new parsing layers must keep accumulating through `Decimal` for fractional accuracy.
- `dozenal_calc.calculate()` tokenizes expressions (numbers using `_ALLOWED_DIGITS`, `+ - * /`, parentheses) then converts each dozenal literal to `Decimal` before shunting-yard evaluation. `CalculatorResult` includes both the `Decimal` and formatted dozenal string, and invalid syntax raises `ValueError` so callers can signal bad input up to the CLI.
- Every CLI tool registers in `src/dozenal/cli.py`'s `_TOOLS` mapping. Arguments live inside tool-specific groups (`dozenal_decimal_converter` vs `dozenal_calc`) with `argparse` ensuring mutual exclusion and clear error messages. Keep new tool flags grouped like this to avoid cluttering the shared namespace.
- Tests rely on `tests/conftest.py` to insert `src/` into `sys.path`, so all new tests belong in `tests/` and should follow the existing pytest style (parameterized cases + explicit `Decimal` expectations) for reliable automation.

## CLI guidance
- The `dozenal` CLI (entry point from `pyproject.toml`) runs `run_cli` in `src/dozenal/cli.py`. `--tool/-t` selects between `converter` and `calculator`, and `--list-tools` prints `_TOOLS` so adding new modules is just a matter of populating that dictionary.
- Use the converter via `dozenal --tool converter --to-doz 3.5` or `dozenal --tool converter --to-dec T`. The CLI enforces that `--to-doz`/`--to-dec` are mutually exclusive and requires at least one when running the converter.
- Use the calculator via `dozenal --tool calculator --calc-expr "1.T + 2"`; output prints both the `Decimal` result and the dozenal string (formatted with `--frac-precision`). The same `--frac-precision` flag controls fractional digits for both tools because both rely on `decimal_to_dozenal`.
- `--list-tools` enumerates the entries in `_TOOLS` (currently `converter` and `calculator`), so newly added tools appear automatically without touching the CLI parser.

## Workflow nuggets
- Run the unit suite with `python -m pytest tests`. No custom runner exists yet, so the standard pytest invocation is the fastest way to confirm conversions and calculator behavior.
- Build or package the project with `uv build` at the repo root because `uv_build` (declared as the build backend) is still required to generate distributable artifacts.
- All CLI development flows through `run_cli`. Keep new functionality inside `cli.py`, add any helper modules under `src/dozenal/`, and register them in `_TOOLS` so the `dozenal` command keeps the same discovery surface.

## Notes for future enhancements
- The calculator currently supports `+ - * /` and parentheses, normalizes unary `+/-` before literals or parentheses (e.g., `-(1+1)`), and relies on the Decimal context precision (`max(28, frac_precision * 3)`) before evaluation. If you expose more operators, keep the shunting-yard and `_PRECEDENCE` table in sync.
- Fractional precision is always passed to `decimal_to_dozenal`, so adjust `--frac-precision` in the CLI to control how many dozenal digits appear whenever a fractional component is present.
- No third-party dependencies exist yet; if you add one (e.g., for parsing expressions), update `pyproject.toml`, regenerate `uv.lock` via `uv sync`, and mention it in these instructions.

Let me know if any section needs clarification or if you'd like me to document additional workflows.