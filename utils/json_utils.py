import json
import os


def save_json(data, file_path, indent=4):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    print(f"JSON saved to {file_path}")


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
