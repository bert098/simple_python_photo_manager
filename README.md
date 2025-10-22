# Image Library CLI

A Python command-line tool for loading, filtering, and searching photo metadata.

## Features
- Load image metadata from CSV
- Filter by multiple tag–value pairs (e.g. `Favorite==Yes`, `DPI>20`)
- Filter by coordinates inside a polygon area
- Combine filters with AND logic
- Print and export results to `results.csv`

## Project Structure
```
image_library_cli/
├─ image_lib/
│  ├─ cli.py, loader.py, coords.py, geometry.py, filters.py
├─ tests/
│  ├─ test_coords.py, test_geometry.py, test_filters.py
├─ app.py
├─ requirements.txt
└─ README.md
```

## Installation

### Windows (PowerShell)
```powershell
git clone https://github.com/<your-user>/image-library-cli.git
cd image-library-cli
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux
```bash
git clone https://github.com/<your-user>/image-library-cli.git
cd image-library-cli
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the program:
```bash
python app.py --csv "images.csv" --tags "Favorite==Yes" "DPI>20"
```

### Arguments

| Flag | Required | Description |
|------|-----------|-------------|
| `--csv` | Yes | Path to metadata CSV |
| `--tags` | No | Tag filters like `"Favorite==Yes" "DPI>20"` |
| `--polygon` | No | List of [lat, lon] pairs for spatial filter |
| `--limit` | No | Max number of rows to display (default 1000) |

### Examples
```bash
# Tag filter
python app.py --csv "images.csv" --tags "Favorite==Yes" "DPI>20"

# Polygon filter
python app.py --csv "images.csv" --polygon "[(51.0,-114.2),(51.0,-113.9),(51.2,-113.9),(51.2,-114.2)]"

# Combined filters
python app.py --csv "images.csv" --tags "Favorite==Yes" "DPI>20" --polygon "[(51.0,-114.2),(51.0,-113.9),(51.2,-113.9),(51.2,-114.2)]"
```

## Running Tests
```bash
pytest -q
```

## Notes
- Wrap CSV file paths with spaces in quotes
- Run tests from the project root (not inside the tests folder)
