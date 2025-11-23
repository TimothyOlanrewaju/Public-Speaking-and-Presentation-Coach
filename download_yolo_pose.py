from ultralytics import YOLO
import shutil
from pathlib import Path

model = YOLO("yolo11n-pose.pt")  

project_root = Path(__file__).parent
target = project_root / "yolo11n-pose.pt"

if not target.exists():
    print("Copying model to project root...")
    shutil.copy2(model.model.path, target)
else:
    print("Model already in project root.")

print(f"Ready: {target.resolve()}")