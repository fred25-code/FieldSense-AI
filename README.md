# FieldSense AI 1.0 — Water Quality & Environmental Intelligence

A Windows desktop MVP for locally managing water-quality sampling documents, extracting candidate measurements with PaddleOCR, applying transparent screening rules, reviewing/correcting values, and exporting Excel/PDF reports.

## What is included

- Native PySide6 desktop UI (no browser or local web server)
- SQLite project, document, sample, measurement, validation, finding, audit and export tables
- Local OCR integration using PaddleOCR with v2/v3 result compatibility
- PDF page rendering with PyMuPDF and image preprocessing with Pillow
- Candidate extraction for pH, temperature, turbidity, conductivity, dissolved oxygen, TDS, salinity, nitrate and phosphate
- Manual data entry, correction, review status and audit trail
- Configurable screening rules (starter ranges are explicitly non-regulatory)
- Excel and PDF exports
- Source documents copied into the local application data folder

## Important offline deployment note

The application makes no network calls for normal operation. PaddleOCR model files and Python dependency packages are not embedded in this source ZIP because PaddlePaddle wheels and OCR models are large and platform-specific. To make a fully offline installation, prepare a `wheelhouse` folder containing compatible Windows wheels and copy the approved PaddleOCR detection and recognition model directories into:

- `models/paddleocr/det/`
- `models/paddleocr/rec/`
- optionally `models/paddleocr/cls/`

The application intentionally refuses to auto-download models. If models are missing, document import, manual entry, SQLite storage, validation, and exports still work; OCR reports that the local models are unavailable.

## Requirements

- Windows 10/11 64-bit
- Python 3.10–3.12 (64-bit)
- For OCR: compatible PaddlePaddle/PaddleOCR wheels and local model directories

## Install

1. Extract this folder to a writable location.
2. Run `install_windows.bat`.
   - If `wheelhouse/` exists, installation uses `pip --no-index` and does not connect to the internet.
   - Otherwise, the setup script downloads dependencies once. After setup, the app itself is offline.
3. Add local PaddleOCR models as described above.
4. Run `run_fieldsense.bat`.

## Database and data location

User data is stored under `%LOCALAPPDATA%\FieldSenseAI\data\` (or the home directory fallback), not in the installation directory. This avoids write-permission issues when installed under Program Files.

## MVP workflow

1. Create/select a project.
2. Import a PNG/JPG/TIFF/BMP/PDF field sheet or lab report.
3. Enter sample ID, collection date and location.
4. Run local OCR. Extracted candidates are saved as `needs_review`.
5. Review/edit each candidate in the Measurements tab and mark it reviewed.
6. Run validation and inspect findings.
7. Export Excel or PDF.

## Database schema

See `fieldsense/schema.sql`. Tables: `projects`, `documents`, `samples`, `measurements`, `validation_rules`, `validation_findings`, `audit_log`, `exports`.

## Known MVP limitations

- OCR parameter parsing is deliberately conservative and line-based; complex multi-column forms and values split across separate lines need human correction.
- Cross-document sample reconciliation, custom rule editor, user accounts/roles, and advanced anomaly models are planned for later releases.
- Starter parameter ranges are generic technical sanity checks, not Ugandan standards, WHO guideline limits, or a drinking-water safety determination. Institutions must configure and approve applicable standards.
- The app stores source file paths and copies imported evidence to its local data directory. Back up `%LOCALAPPDATA%\FieldSenseAI\data\` regularly.

## Development checks

Run `python -m unittest discover -s tests` from this directory.
