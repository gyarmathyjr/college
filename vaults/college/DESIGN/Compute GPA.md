
# GPA Computation Requirements

## Purpose

Compute university-specific GPAs from a transcript DataFrame using declarative GPA policy files.  
Each run should (re)compute GPAs for all configured universities and persist results to a single summary artifact.

Create a script that will compute the grades
Create a notebook in the notebooks folder to view the computed grades


---

## Inputs

### 1. GPA Policies

- **Location:** `data/gpa_policies/`
    
- **Format:** one JSON file per university
    
- **Each policy defines:**
    
    - letter → numeric grade scale
        
    - which grade columns are eligible
        
    - how missing grades are handled
        
    - how credits weight grades
        
    - inclusion/exclusion logic based on a DataFrame dimension (e.g., `requirement_area`)
        
    - rounding rules
        

No policy inference is allowed.  
Only rules explicitly defined in the policy may be applied.

---

### 2. Transcript Data

- **Structure:** tabular (DataFrame-like)
    
- **Required columns:**
    
    - `requirement_area`
        
    - `credits`
        
    - grade columns (e.g., `grades.S1`, `grades.S2`, `grades.Q1`, etc.)
        
- **Grade values:** letter grades or `None` / null
    

The transcript is treated as authoritative.

---

## Processing Logic

For **each GPA policy file** in `data/gpa_policies/`:

### Step 1 — Load policy

- Parse policy JSON
    
- Validate required sections:
    
    - `grade_scale`
        
    - `grade_selection`
        
    - `credit_policy`
        
    - `course_inclusion`
        
    - `calculation`
        

Fail fast if invalid.

---

### Step 2 — Select eligible grade cells

- Use only grade columns listed in `grade_selection.use_columns`
    
- Ignore:
    
    - columns in `ignore_columns`
        
    - values in `ignore_values` (e.g., `None`, null)
        
- Each **non-missing semester grade** is treated as a separate graded unit
    

---

### Step 3 — Apply course inclusion rules

- Use `course_inclusion.dimension` to filter rows (e.g., `requirement_area`)
    
- If `include_all_credit_bearing_courses = true`:
    
    - include all rows except those explicitly excluded
        
- Otherwise:
    
    - exclude rows where `dimension ∈ exclude_values`
        

No subject inference or heuristics.

---

### Step 4 — Convert grades to numeric values

- Map each letter grade using `grade_scale`
    
- Grades not present in the scale cause a hard error
    

---

### Step 5 — Weight by credits

- Weight numeric grades using `credit_policy.weight_by`
    
- Credit unit is defined by `credit_policy.credit_unit`
    
- Each semester grade contributes:
    
    ```
    numeric_grade × credits
    ```
    

---

### Step 6 — Compute GPA

- Use `calculation.method` (currently `weighted_mean`)
    
- GPA formula:
    
    ```
    sum(numeric_grade × credits) / sum(credits)
    ```
    
- Apply rounding rules from `calculation.rounding`
    

---

## Outputs

### GPA Summary File

- **Location:** `data/gpa_summary.json`
    
- **Behavior:** create if missing, update if exists
    
- **Structure:**
    

```json
{
  "last_updated": "ISO-8601 timestamp",
  "gpas": {
    "University of Washington": {
      "campus": "Seattle",
      "gpa": 3.72,
      "policy_version": "2024-UG",
      "credits_counted": 14.0,
      "grades_counted": 28
    }
  }
}
```

- One entry per policy file
    
- Recomputed on every run (no caching)
    
