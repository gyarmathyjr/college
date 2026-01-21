# College

A Python-based tool for calculating GPA (Grade Point Average) according to different university admission policies. This repository helps students understand how their transcript will be evaluated by various colleges and universities, each of which may use different GPA calculation methodologies.

## Purpose

This project enables students to:
- Calculate their GPA according to multiple university-specific policies
- Understand how different institutions evaluate transcripts
- Compare GPA results across different schools
- Maintain consistent GPA calculations using policy version control

## Currently Implemented Functionality

### GPA Calculator Module (`modules/gpa_calculator.py`)

The core functionality includes:

- **Transcript Loading**: Load student transcript data from JSON format
- **Multi-Policy Support**: Calculate GPA according to different university policies
- **Flexible Grade Selection**: Handle different grading systems (semester, quarter, etc.)
- **Course Filtering**: Exclude specific courses based on policy requirements
- **Configurable Grade Scales**: Support various letter grade to numeric conversions
- **Validation**: Detect and prevent common data issues (missing columns, duplicate grades)

### Key Features

1. **Policy-Based Calculations**: Each university's GPA calculation rules are defined in JSON policy files located in `data/gpa_policies/`

2. **Grade Scale Mapping**: Converts letter grades to numeric values according to each school's specific scale

3. **Selective Grade Counting**: Handles transcripts with multiple grading periods (quarters, semesters) and selects appropriate grades per policy

4. **Credit Weighting**: Properly weights grades by course credits

5. **Precision Control**: Configurable rounding precision for GPA results

### Data Structure

- `data/transcript.json` - Student transcript with course history
- `data/gpa_policies/*.json` - University-specific GPA calculation policies
- `data/gpa_summary.json` - Computed GPA results for all policies
- `data/admissions_policies/*.json` - Admission policy reference data

### Scripts

- `scripts/compute_gpa.py` - Main script to calculate GPAs using all policies

### Tests

- `tests/test_gpa_validation.py` - Unit tests for GPA calculation validation

### Notebooks

- Jupyter notebooks for interactive analysis and exploration of transcript data

## Current University Policies Supported

Based on the GPA summary, policies are implemented for:
- University of Washington (Seattle)
- Western Washington University (Bellingham)
- Washington State University (Pullman)
- University of California, Davis
- California Polytechnic State University (San Luis Obispo)
- San Diego State University
- Seattle University

## Usage

1. Place your transcript data in `data/transcript.json`
2. Configure or add university policies in `data/gpa_policies/`
3. Run the GPA calculation:
   ```bash
   python scripts/compute_gpa.py
   ```
4. View results in `data/gpa_summary.json`

## Requirements

- Python >= 3.13
- pandas >= 2.3.3
- notebook >= 7.5.2

## Project Structure

```
college/
├── modules/
│   └── gpa_calculator.py    # Core GPA calculation logic
├── data/
│   ├── transcript.json      # Student transcript data
│   ├── gpa_policies/        # University GPA policies
│   ├── admissions_policies/ # Admission requirements
│   └── gpa_summary.json     # Calculated results
├── scripts/
│   └── compute_gpa.py       # Main computation script
├── tests/
│   └── test_gpa_validation.py  # Unit tests
├── notebooks/               # Jupyter notebooks for analysis
└── vaults/                  # Additional data storage
```
