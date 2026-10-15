import json
from pathlib import Path

def write_json(records:list[dict],output_path:Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path,"w",encoding="utf-8") as file:
        json.dump(records, file, indent=2)