"""
app.py - Annotation tool backend.

Serves the frontend, lists frames, and reads/writes YOLO-format label files.

Run:
    pip install fastapi uvicorn python-multipart
    python app.py

Then open http://localhost:8000 in your browser.

Directory layout expected (created automatically if missing):
    frames/     - your extracted .jpg frames (from extract_frames.py)
    labels/     - YOLO .txt label files, one per frame, same basename
    classes.txt - one class name per line, in class-index order
"""

import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent
FRAMES_DIR = BASE_DIR / "frames"
LABELS_DIR = BASE_DIR / "labels"
CLASSES_FILE = BASE_DIR / "classes.txt"

FRAMES_DIR.mkdir(exist_ok=True)
LABELS_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Vehicle Annotation Tool")

IMG_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class Box(BaseModel):
    class_id: int
    cx: float  # normalized center x (0-1)
    cy: float  # normalized center y (0-1)
    w: float   # normalized width (0-1)
    h: float   # normalized height (0-1)


class LabelPayload(BaseModel):
    boxes: List[Box]


def get_frame_list() -> List[str]:
    return sorted([
        f.name for f in FRAMES_DIR.iterdir()
        if f.suffix.lower() in IMG_EXTENSIONS
    ])


def get_classes() -> List[str]:
    if not CLASSES_FILE.exists():
        return ["vehicle"]
    lines = [l.strip() for l in CLASSES_FILE.read_text().splitlines()]
    return [l for l in lines if l]


def label_path_for(frame_name: str) -> Path:
    stem = Path(frame_name).stem
    return LABELS_DIR / f"{stem}.txt"


@app.get("/api/state")
def api_state():
    frames = get_frame_list()
    classes = get_classes()
    annotated = set()
    for f in frames:
        lp = label_path_for(f)
        if lp.exists() and lp.read_text().strip():
            annotated.add(f)
    return {
        "frames": frames,
        "classes": classes,
        "annotated_count": len(annotated),
        "total_count": len(frames),
        "annotated": sorted(annotated),
    }


@app.get("/api/label/{frame_name}")
def api_get_label(frame_name: str):
    lp = label_path_for(frame_name)
    boxes = []
    if lp.exists():
        for line in lp.read_text().strip().splitlines():
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            class_id, cx, cy, w, h = parts
            boxes.append({
                "class_id": int(class_id),
                "cx": float(cx),
                "cy": float(cy),
                "w": float(w),
                "h": float(h),
            })
    return {"boxes": boxes}


@app.post("/api/label/{frame_name}")
def api_save_label(frame_name: str, payload: LabelPayload):
    if frame_name not in get_frame_list():
        raise HTTPException(status_code=404, detail="Frame not found")

    lp = label_path_for(frame_name)
    lines = []
    for b in payload.boxes:
        lines.append(f"{b.class_id} {b.cx:.6f} {b.cy:.6f} {b.w:.6f} {b.h:.6f}")

    if lines:
        lp.write_text("\n".join(lines) + "\n")
    else:
        # No boxes -> remove label file (empty frame, e.g. no vehicles)
        if lp.exists():
            lp.unlink()

    return {"status": "ok", "saved_boxes": len(lines)}


@app.get("/frames/{frame_name}")
def get_frame_image(frame_name: str):
    fp = FRAMES_DIR / frame_name
    if not fp.exists():
        raise HTTPException(status_code=404, detail="Frame not found")
    return FileResponse(fp)


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    return (BASE_DIR / "static" / "index.html").read_text()


if __name__ == "__main__":
    import uvicorn
    print(f"Frames dir:  {FRAMES_DIR}")
    print(f"Labels dir:  {LABELS_DIR}")
    print(f"Classes:     {get_classes()}")
    print(f"Found {len(get_frame_list())} frame(s).")
    print("\nOpen http://localhost:8000 in your browser.\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
