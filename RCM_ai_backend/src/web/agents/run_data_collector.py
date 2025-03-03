#!/usr/bin/env python
import os
import sys
import json
import argparse
from pathlib import Path

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the data collector
from data_collector import DataCollectorCrew, process_file, process_directory

def main():
    """
    Main function to run the data collector agent.
    """
    parser = argparse.ArgumentParser(description='Medical Data Collector Agent')
    
    # Add arguments
    parser.add_argument('--file', type=str, help='Path to a single file to process')
    parser.add_argument('--dir', type=str, help='Path to a directory of files to process')
    parser.add_argument('--output', type=str, help='Path to save the output JSON')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if at least one input is provided
    if not args.file and not args.dir:
        print("Error: Please provide either a file (--file) or directory (--dir) to process.")
        parser.print_help()
        sys.exit(1)
    
    # Process based on input type
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File {args.file} does not exist.")
            sys.exit(1)
        
        print(f"Processing file: {args.file}")
        result = process_file(args.file)
    else:
        if not os.path.exists(args.dir):
            print(f"Error: Directory {args.dir} does not exist.")
            sys.exit(1)
        
        print(f"Processing directory: {args.dir}")
        result = process_directory(args.dir)
    
    # Print result if verbose
    if args.verbose:
        print(json.dumps(result, indent=2))
    
    # Save output if specified
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Results saved to: {args.output}")
    
    print("Processing complete!")

if __name__ == "__main__":
    main() 