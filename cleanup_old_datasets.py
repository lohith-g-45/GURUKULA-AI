import sys
import os
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from utils.dataset_manager import cleanup_old_structure


def main():
    print("=" * 80)
    print("GURUKULA AI - DATASET CLEANUP")
    print("=" * 80)
    
    cleanup_old_structure()
    
    print("\nCleanup complete!")


if __name__ == "__main__":
    main()
