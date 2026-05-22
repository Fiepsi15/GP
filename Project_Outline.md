# AGENTS.md - GitHub Copilot Guide for GP Physics Lab Analysis

## Project Overview
**GP** is a physics lab experiment data analysis project for the "Grundpraktikum Physik" at Universität Ulm. It processes experimental measurements from physics lab sessions into analyzed results with uncertainty quantification and LaTeX-formatted reports.

### Project Structure
```
_1a/          # Series 1a: Mechanics (individual script files)
_1b/          # Series 1b: Mechanics (modular experiments)
_1c/          # Series 1c: Electricity (modular experiments)
_2/           # Series 2: Optics (modular experiments)
scrips/       # Shared utilities: LaTeX generation, scientific rounding
```

## Architecture Patterns

### Modular Experiment Structure (Series _1b, _1c, _2)
**Pattern**: Each experiment is a self-contained module with a consistent layout:

```
_XX_ExperimentName/
├── main.py              # Entry point - runs full analysis pipeline
├── subscripts/          # Calculation functions (imported locally)
│   ├── calcs.py        # Core calculations with error propagation
│   ├── physics_function.py
│   └── __init__.py
├── daten/              # CSV experimental data files
│   ├── measurement_1.csv
│   └── measurement_2.csv
└── __init__.py
```

**Key principle**: All files within a module are imported using absolute paths from project root:
- `from _1b._01_Reversionspendel.subscripts.unsicherheit import get_unsicherheit`
- `from _1b._02_Gekoppeltes_Pendel.subscripts.calcs import get_Traegheitsmoment_from_Parameters`

### Data Processing Pipeline
1. **Load CSV data** via `np.loadtxt(path, skiprows=1, delimiter=',')`
2. **Calculate measurements** with error propagation
3. **Generate LaTeX tables** using `scrips.array_to_tex` functions
4. **Visualize results** with matplotlib

**Example from `_1b/_01_Reversionspendel/main.py`**:
```python
# Load data with units (mm, s)
L_1 = daten_Aufhaengung_1[0] * 1e-3  # Convert to meters
T_1 = daten_Aufhaengung_1[1] / 50     # Divide by 50 (averaging)

# Calculate with uncertainties
k1, d_k1, b1, d_b1 = linear_regression_pendulum(T_1, dT_1, L_1, dL_1)

# Generate LaTeX table
a2t.csv_to_tex('path/to/data.csv', [error_arrays], 
                [['L', 'T'], ['m', 's']], 'Caption', 'label')
```

## Critical Conventions & Patterns

### 1. **Unit Conversions Are Explicit**
- Raw CSV data is in mixed units; always convert immediately:
  - Millimeters → meters: `* 1e-3`
  - Measurements per 50 cycles → single period: `/ 50`
  - This occurs in nearly every main.py at data loading

### 2. **Error Propagation Is Central**
- **Every measurement has paired uncertainty data** (value, delta_value)
- Errors are propagated through calculations, not ignored
- Scientific rounding uses `scrips.tools.sci_round(value, error)` to round both value and error together
- Study subscripts modules for error propagation formulas specific to each experiment

### 3. **LaTeX Table Generation**
- Core function: `array_to_tex.array_to_tex(array, error_array, quantities_and_units, caption, label)`
- Also supports deprecated `csv_to_tex()` for direct CSV conversion
- Output: prints to console AND writes to `tex_data.txt` in project root
- Input structure: `quantities_and_units = [['$L$', '$T$'], ['m', 's']]`
- Errors displayed as: `\SI{value ± error}{}`

### 4. **Subscript Module Organization**
Common patterns in subscripts:
- `calcs.py` or `pendel.py`: Core physics calculations
- `unsicherheit.py`: Uncertainty calculations from raw measurements
- Single responsibility; functions are frequently called from main.py
- Functions accept both value arrays and error arrays as parallel parameters

### 5. **Parameter-Based vs. Measurement-Based Calculations**
Two calculation paths exist in some experiments:
- **From parameters** (theoretical): `get_X_from_Parameters(m_Z, L_Z, ...)`  
- **From oscillation** (experimental): `get_X_from_oscillation(omega_P, omega_G, ...)`

Example: `_1b/_02_Gekoppeltes_Pendel` calculates moment of inertia both ways for comparison.

## Shared Utilities (`scrips/` directory)

### `array_to_tex.py` - LaTeX Table Generation
- **`array_to_tex()`**: numpy 2D arrays → LaTeX tables with error columns
- **`csv_to_tex()`**: CSV files → LaTeX tables (deprecated)
- Automatic row layout optimization (tries 3-5 columns per section)
- Applies scientific rounding to all data before formatting
- Always outputs to `tex_data.txt`

### `tools.py` - Scientific Utilities
- **`sci_round(value, error)`**: Rounds value and error with respect to error's first significant digit
- **`round_up()`**: Ceiling rounding to decimal places
- **`find_first_nonzero_digit()`**: Utility for scientific notation handling

## File Patterns & Naming

### CSV Data Files
- Located in `daten/` subdirectories
- Format: comma-delimited, first row is header
- Typically contain repeated measurements (e.g., 10 cycles, then divide by 10)

### Python Files
- Some experiments have modular `main.py` (preferred: _1b, _1c, _2)
- Some have standalone analysis scripts in parent (older: _1a files like `Fadenpendel.py`)
- Subscript functions typically use German physics terminology

### Output
- LaTeX tables written to project root `tex_data.txt` (overwrites each run)
- Matplotlib figures displayed with `.show()`
- Print statements to console for inspection of intermediate values

## Common Workflow

**Adding/Modifying an Experiment**:
1. Ensure CSV data is in `_XX_ExperimentName/daten/` with proper headers
2. Create calculation functions in `subscripts/calcs.py` with paired error parameters
3. In `main.py`, load data → convert units → call subscript functions → generate tables
4. Use `array_to_tex.array_to_tex()` to format results for LaTeX reports
5. Test by running `main.py` and verifying output in console + `tex_data.txt`

**Error Propagation**:
- Pass error arrays parallel to value arrays through function calls
- Functions return `(value, error)` tuples or paired arrays
- Use NumPy operations to propagate `sqrt(a² + b²)` patterns

## Dependencies
- NumPy: Array operations and CSV loading
- Matplotlib: Plotting and visualization
- No external frameworks; pure scientific Python

## Notes for AI Agents
- **Absolute imports required**: Always use full path from project root
- **German terminology**: Physics terms in German; variable names often use German
- **Units are critical**: Conversion errors invalidate analyses; verify early
- **Error propagation non-negotiable**: Never drop uncertainty; calculate it through every step
- **LaTeX output primary**: Results feed into physics reports; formatting matters

