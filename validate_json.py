
import os
import json

def validate_json_files(root_dir):
    issues = []
    json_files = []
    
    # Find all JSON files
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.json'):
                json_files.append(os.path.join(dirpath, filename))
    
    print(f"Found {len(json_files)} JSON files to validate...\n")
    
    for file_path in json_files:
        print(f"Validating: {os.path.relpath(file_path, root_dir)}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            print("  [OK] Valid JSON")
        except json.JSONDecodeError as e:
            print(f"  [ERROR] Invalid JSON: {e}")
            issues.append((file_path, f"JSON decode error: {e}"))
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            issues.append((file_path, f"Error: {e}"))
    
    # Summary
    print("\n" + "="*50)
    if issues:
        print(f"\nFound {len(issues)} issues:")
        for file, issue in issues:
            print(f"  - {os.path.relpath(file, root_dir)}: {issue}")
    else:
        print("\n[SUCCESS] All JSON files are valid!")
    
    return len(issues) == 0

if __name__ == "__main__":
    kas_dir = os.path.join(os.path.dirname(__file__), "datasets", "KAS")
    validate_json_files(kas_dir)

