

## ⚠️ Real concerns (ordered by severity)

### 1️⃣ **Potential double-counting if a row ever has both S1 and S2**

Right now:

```python
for _, row in df.iterrows():
    credits = row.get("credits", 0.0)
    for col in use_columns:
        total_weighted_points += numeric_grade * credits
        total_credits += credits
```

If **one row contains both S1 and S2**, you will:

- count **credits twice**
    
- inflate GPA weight
    

You _believe_ your data is one-semester-per-row — but the code assumes it.

**Fix (minimal, safe):**  
Add a guard:

```python
non_null_grades = [
    col for col in use_columns
    if row.get(col) not in ignore_values
]

if len(non_null_grades) > 1:
    raise ValueError("Row contains multiple semester grades; ambiguous credit allocation")
```

This enforces your data contract explicitly.

---

### 2️⃣ `ignore_values` check is slightly unsafe

You do:

```python
if grade_letter in ignore_values:
    continue
```

If:

- `grade_letter` is `NaN` (pandas)
    
- or empty string `""`
    

This may slip through.

**Safer:**

```python
if pd.isna(grade_letter) or grade_letter in ignore_values:
    continue
```

This avoids silent grade pollution.

---

### 3️⃣ No validation that grade columns exist

If a policy says:

```json
"use_columns": ["grades.S1", "grades.S2"]
```

and the transcript schema changes, you’ll silently get `None` for all rows.

**Add once, early in `calculate_gpa`:**

```python
missing = [c for c in use_columns if c not in df.columns]
if missing:
    raise KeyError(f"Missing grade columns: {missing}")
```

This is important for extensibility.

---

### 4️⃣ `grades_counted` is semantically ambiguous

You increment:

```python
grades_counted += 1
```

That currently means:

> number of **semester grades** included

That’s fine — but document it.  
Right now a reader could assume “courses counted”.

**Suggestion (no code change required):**  
Rename in output (later if you want):

- `semester_grades_counted`
    

Your math is already correct.
