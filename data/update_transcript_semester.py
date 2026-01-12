import json

# Load the JSON data
file_path = '/Users/jamesgyarmathy/Code/college/data/transcript.json'
with open(file_path, 'r') as f:
    data = json.load(f)

# Iterate through course history and add semester field
for course in data['course_history']:
    grades = course.get('grades', {})
    
    # Check for presence of grades in Q1/Q2 or Q3/Q4
    has_q1_q2 = grades.get('Q1') is not None or grades.get('Q2') is not None
    has_q3_q4 = grades.get('Q3') is not None or grades.get('Q4') is not None
    
    if has_q1_q2:
        course['semester'] = 1
    elif has_q3_q4:
        course['semester'] = 2
    else:
        course['semester'] = None

# Write the updated JSON back to file
with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Successfully added semester field to transcript.json")
