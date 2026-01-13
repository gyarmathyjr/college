import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.gpa_calculator import GpaCalculator, load_transcript

def main():
    transcript_path = '/Users/jamesgyarmathy/Code/college/data/transcript.json'
    policies_dir = '/Users/jamesgyarmathy/Code/college/data/gpa_policies'
    output_path = '/Users/jamesgyarmathy/Code/college/data/gpa_summary.json'
    
    try:
        print(f"Loading transcript from {transcript_path}...")
        df = load_transcript(transcript_path)
        print(f"Loaded {len(df)} course entries.")
        
        calculator = GpaCalculator(df, policies_dir)
        print(f"Computing GPAs using policies in {policies_dir}...")
        
        summary = calculator.calculate_all()
        
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
            
        print(f"GPA calculation complete. Results saved to {output_path}")
        print(json.dumps(summary, indent=2))
        
    except Exception as e:
        print(f"Error computing GPA: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
