import json
import pandas as pd
import glob
import os
from datetime import datetime

def load_transcript(file_path):
    """
    Loads transcript data from a JSON file and returns it as a flattened DataFrame.
    
    Args:
        file_path (str): Path to the transcript JSON file.
        
    Returns:
        pd.DataFrame: Flattened DataFrame containing course history.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    df = pd.json_normalize(data['course_history'])
    return df

class GpaCalculator:
    def __init__(self, transcript_df, policies_dir):
        """
        Initialize the GpaCalculator.

        Args:
            transcript_df (pd.DataFrame): The student's transcript data.
            policies_dir (str): Directory containing GPA policy JSON files.
        """
        self.transcript_df = transcript_df
        self.policies_dir = policies_dir
        self.results = {}

    def load_policies(self):
        """Yields policy dictionaries from the policies directory."""
        policy_files = glob.glob(os.path.join(self.policies_dir, "*.json"))
        for p_file in policy_files:
            with open(p_file, 'r') as f:
                yield json.load(f)

    def calculate_all(self):
        """Computes GPA for all loaded policies."""
        timestamp = datetime.now().isoformat()
        
        summary = {
            "last_updated": timestamp,
            "gpas": {}
        }

        for policy in self.load_policies():
            school_name = policy.get("school")
            gpa_data = self.calculate_gpa(policy)
            
            if school_name:
                summary["gpas"][school_name] = gpa_data
        
        return summary

    def calculate_gpa(self, policy):
        """
        Calculates GPA for a single policy.
        
        Args:
            policy (dict): The GPA policy definition.
            
        Returns:
            dict: The computed GPA result.
        """
        df = self.transcript_df.copy()
        
        # 1. Course Inclusion
        inclusion = policy.get("course_inclusion", {})
        dimension = inclusion.get("dimension")
        exclude_values = inclusion.get("exclude_values", [])
        
        if dimension and exclude_values:
            df = df[~df[dimension].isin(exclude_values)]
            
        # 2. Select Eligible Grade Cells & 3. Convert to Numeric
        # We need to iterate through rows and columns to gather all valid grades
        
        grade_scale = policy.get("grade_scale", {})
        use_columns = policy.get("grade_selection", {}).get("use_columns", [])
        ignore_values = set(policy.get("grade_selection", {}).get("ignore_values", [None]))
        
        # 3. Validate existence of required grade columns
        missing_columns = [col for col in use_columns if col not in df.columns]
        if missing_columns:
            raise KeyError(f"Missing grade columns for {policy.get('school')}: {missing_columns}")
        
        total_weighted_points = 0.0
        total_credits = 0.0
        grades_counted = 0
        
        for _, row in df.iterrows():
            credits = row.get("credits", 0.0)
            
            # Identify valid grades for this row
            valid_grades_in_row = []
            
            for col in use_columns:
                grade_letter = row.get(col)
                
                # Check filter ignore values safely
                if pd.isna(grade_letter) or grade_letter in ignore_values:
                    continue
                    
                valid_grades_in_row.append(grade_letter)

            # Prevent double counting
            if len(valid_grades_in_row) > 1:
                raise ValueError(f"Row contains multiple semester grades {valid_grades_in_row}; ambiguous credit allocation for course {row.get('course_name', 'Unknown')}")
            
            if not valid_grades_in_row:
                continue
                
            # Process the single valid grade
            grade_letter = valid_grades_in_row[0]
            
            if grade_letter not in grade_scale:
                raise ValueError(f"Grade '{grade_letter}' not found in grade scale for {policy.get('school')}")
            
            numeric_grade = grade_scale[grade_letter]
            
            total_weighted_points += numeric_grade * credits
            total_credits += credits
            grades_counted += 1
                
        # 5. Compute GPA
        if total_credits == 0:
            gpa = 0.0
        else:
            gpa = total_weighted_points / total_credits
            
        # 6. Rounding
        rounding = policy.get("calculation", {}).get("rounding", {})
        precision = rounding.get("precision", 2)
        
        gpa = round(gpa, precision)
        
        return {
            "campus": policy.get("campus"),
            "gpa": gpa,
            "policy_version": policy.get("gpa_policy_version"),
            "credits_counted": round(total_credits, 2),
            "semester_grades_counted": grades_counted
        }
