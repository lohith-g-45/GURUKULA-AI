import os
import shutil

def migrate_kas():
    old_dirs = [
        "exams",
        "syllabus",
        "weightage",
        "patterns",
        "pyqs",
        "raw",
        "analytics",
        "agent_contexts"
    ]
    
    new_kas_base = "datasets/KAS"
    os.makedirs(new_kas_base, exist_ok=True)
    
    for old_dir in old_dirs:
        old_path = os.path.join("datasets", old_dir)
        new_path = os.path.join(new_kas_base, old_dir)
        
        if os.path.exists(old_path):
            shutil.copytree(old_path, new_path, dirs_exist_ok=True)
            print(f"Migrated {old_dir} to {new_path}")
    
    print("\nKAS datasets migrated successfully!")
    
if __name__ == "__main__":
    migrate_kas()
