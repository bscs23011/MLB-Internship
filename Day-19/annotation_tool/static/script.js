// ---- State ----
let frames = [];
let classes = [];
let currentIndex = 0;
let currentBoxes = []; // {class_id, cx, cy, w, h} normalized
let activeClassId = 0;
let img = new Image();
let scale = 1; // displayed size / natural size

// drawing state
let isDrawing = false;
let drawStartX = 0;
let drawStartY = 0;

// selection / edit state
let selectedIndex = null;
let mode = null; // null | "drawing" | "moving" | "resizing"
let resizeHandle = null; // "nw" | "ne" | "sw" | "se"
let dragStartX = 0;
let dragStartY = 0;
let dragOrigBox = null; // snapshot of box (in px) at drag start

const HANDLE_SIZE = 8;

const CLASS_COLORS = [
  "#f87171", "#fb923c", "#facc15", "#4ade80",
  "#38bdf8", "#a78bfa", "#f472b6", "#94a3b8", "#2dd4bf"
];

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const classSelect = document.getElementById("class-select");
const boxList = document.getElementById("box-list");
const noBoxesMsg = document.getElementById("no-boxes-msg");
const progressEl = document.getElementById("progress");
const filenameEl = document.getElementById("filename");
const saveBtn = document.getElementById("save-btn");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");

async function init() {
  const res = await fetch("/api/state");
  const state = await res.json();
  frames = state.frames;
  classes = state.classes;

  if (frames.length === 0) {
    progressEl.textContent = "No frames found in frames/ folder.";
    return;
  }

  classSelect.innerHTML = classes
    .map((c, i) => `<option value="${i}">${i + 1}: ${c}</option>`)
    .join("");
  classSelect.addEventListener("change", () => {
    activeClassId = parseInt(classSelect.value, 10);
  });

  updateProgress(state.annotated_count, state.total_count);
  await loadFrame(0);
}

function updateProgress(annotatedCount, totalCount) {
  progressEl.textContent = `${annotatedCount} / ${totalCount} frames annotated`;
}

async function refreshProgress() {
  const res = await fetch("/api/state");
  const state = await res.json();
  updateProgress(state.annotated_count, state.total_count);
}

async function loadFrame(index) {
  if (index < 0 || index >= frames.length) return;
  currentIndex = index;
  const frameName = frames[currentIndex];
  filenameEl.textContent = `${currentIndex + 1}/${frames.length} — ${frameName}`;

  // load image
  await new Promise((resolve) => {
    img.onload = resolve;
    img.src = `/frames/${frameName}?t=${Date.now()}`;
  });

  // fit canvas to a max display size while keeping aspect ratio
  const maxW = Math.min(window.innerWidth - 340, 1100);
  const maxH = window.innerHeight - 100;
  scale = Math.min(maxW / img.naturalWidth, maxH / img.naturalHeight, 1);
  canvas.width = img.naturalWidth * scale;
  canvas.height = img.naturalHeight * scale;

  // load existing boxes
  const res = await fetch(`/api/label/${frameName}`);
  const data = await res.json();
  currentBoxes = data.boxes || [];
  selectedIndex = null;
  mode = null;

  render();
  saveBtn.classList.remove("saved");
  saveBtn.textContent = "Save (S)";
}

function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

  currentBoxes.forEach((b, i) => drawBox(b, i));
  renderBoxList();
}

function boxToPx(b) {
  return {
    x: (b.cx - b.w / 2) * canvas.width,
    y: (b.cy - b.h / 2) * canvas.height,
    w: b.w * canvas.width,
    h: b.h * canvas.height,
  };
}

function pxToBox(px, classId) {
  return {
    class_id: classId,
    cx: (px.x + px.w / 2) / canvas.width,
    cy: (px.y + px.h / 2) / canvas.height,
    w: px.w / canvas.width,
    h: px.h / canvas.height,
  };
}

function drawBox(b, index) {
  const color = CLASS_COLORS[b.class_id % CLASS_COLORS.length];
  const { x, y, w, h } = boxToPx(b);
  const isSelected = index === selectedIndex;

  ctx.strokeStyle = color;
  ctx.lineWidth = isSelected ? 3 : 2;
  ctx.strokeRect(x, y, w, h);

  const label = classes[b.class_id] || `class ${b.class_id}`;
  ctx.font = "12px sans-serif";
  const textW = ctx.measureText(label).width + 8;
  ctx.fillStyle = color;
  ctx.fillRect(x, Math.max(0, y - 16), textW, 16);
  ctx.fillStyle = "#0a0a0a";
  ctx.fillText(label, x + 4, Math.max(12, y - 4));

  if (isSelected) {
    drawHandles(x, y, w, h, color);
  }
}

function drawHandles(x, y, w, h, color) {
  const corners = [[x, y], [x + w, y], [x, y + h], [x + w, y + h]];
  ctx.fillStyle = color;
  corners.forEach(([hx, hy]) => {
    ctx.fillRect(hx - HANDLE_SIZE / 2, hy - HANDLE_SIZE / 2, HANDLE_SIZE, HANDLE_SIZE);
  });
}

function getHandleAt(px, py, boxPx) {
  const { x, y, w, h } = boxPx;
  const corners = {
    nw: [x, y], ne: [x + w, y], sw: [x, y + h], se: [x + w, y + h],
  };
  for (const [name, [hx, hy]] of Object.entries(corners)) {
    if (Math.abs(px - hx) <= HANDLE_SIZE && Math.abs(py - hy) <= HANDLE_SIZE) {
      return name;
    }
  }
  return null;
}

function isInsideBox(px, py, boxPx) {
  return px >= boxPx.x && px <= boxPx.x + boxPx.w &&
         py >= boxPx.y && py <= boxPx.y + boxPx.h;
}

function renderBoxList() {
  boxList.innerHTML = "";
  noBoxesMsg.style.display = currentBoxes.length === 0 ? "block" : "none";

  currentBoxes.forEach((b, i) => {
    const li = document.createElement("li");
    if (i === selectedIndex) li.classList.add("selected");
    const color = CLASS_COLORS[b.class_id % CLASS_COLORS.length];
    const label = classes[b.class_id] || `class ${b.class_id}`;
    li.innerHTML = `
      <span><span class="swatch" style="background:${color}"></span>${label}</span>
      <button data-index="${i}">delete</button>
    `;
    li.addEventListener("click", () => {
      selectedIndex = i;
      render();
    });
    li.querySelector("button").addEventListener("click", (e) => {
      e.stopPropagation();
      const idx = parseInt(e.target.dataset.index, 10);
      currentBoxes.splice(idx, 1);
      if (selectedIndex === idx) selectedIndex = null;
      else if (selectedIndex !== null && selectedIndex > idx) selectedIndex--;
      render();
    });
    boxList.appendChild(li);
  });
}

// ---- Drawing / selecting / moving / resizing interactions ----
function getMousePos(e) {
  const rect = canvas.getBoundingClientRect();
  return { x: e.clientX - rect.left, y: e.clientY - rect.top };
}

canvas.addEventListener("mousedown", (e) => {
  const { x: mx, y: my } = getMousePos(e);

  // 1. if a box is currently selected, check if we're grabbing one of its resize handles
  if (selectedIndex !== null) {
    const boxPx = boxToPx(currentBoxes[selectedIndex]);
    const handle = getHandleAt(mx, my, boxPx);
    if (handle) {
      mode = "resizing";
      resizeHandle = handle;
      dragOrigBox = boxPx;
      dragStartX = mx;
      dragStartY = my;
      return;
    }
  }

  // 2. check if click landed inside any existing box (topmost/last drawn wins) -> select + start moving
  for (let i = currentBoxes.length - 1; i >= 0; i--) {
    const boxPx = boxToPx(currentBoxes[i]);
    if (isInsideBox(mx, my, boxPx)) {
      selectedIndex = i;
      mode = "moving";
      dragOrigBox = boxPx;
      dragStartX = mx;
      dragStartY = my;
      render();
      return;
    }
  }

  // 3. otherwise, start drawing a brand new box, and deselect
  selectedIndex = null;
  mode = "drawing";
  drawStartX = mx;
  drawStartY = my;
  render();
});

canvas.addEventListener("mousemove", (e) => {
  if (!mode) return;
  const { x: mx, y: my } = getMousePos(e);

  if (mode === "drawing") {
    render();
    ctx.strokeStyle = "#3b82f6";
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 3]);
    ctx.strokeRect(
      Math.min(drawStartX, mx),
      Math.min(drawStartY, my),
      Math.abs(mx - drawStartX),
      Math.abs(my - drawStartY)
    );
    ctx.setLineDash([]);
  } else if (mode === "moving") {
    const dx = mx - dragStartX;
    const dy = my - dragStartY;
    let newX = dragOrigBox.x + dx;
    let newY = dragOrigBox.y + dy;
    // keep box within canvas bounds
    newX = Math.max(0, Math.min(newX, canvas.width - dragOrigBox.w));
    newY = Math.max(0, Math.min(newY, canvas.height - dragOrigBox.h));
    const newBoxPx = { x: newX, y: newY, w: dragOrigBox.w, h: dragOrigBox.h };
    currentBoxes[selectedIndex] = pxToBox(newBoxPx, currentBoxes[selectedIndex].class_id);
    render();
  } else if (mode === "resizing") {
    const dx = mx - dragStartX;
    const dy = my - dragStartY;
    let { x, y, w, h } = dragOrigBox;

    if (resizeHandle === "se") { w = w + dx; h = h + dy; }
    else if (resizeHandle === "sw") { x = x + dx; w = w - dx; h = h + dy; }
    else if (resizeHandle === "ne") { w = w + dx; y = y + dy; h = h - dy; }
    else if (resizeHandle === "nw") { x = x + dx; w = w - dx; y = y + dy; h = h - dy; }

    // prevent inverted/negative boxes
    if (w > 5 && h > 5) {
      const newBoxPx = { x, y, w, h };
      currentBoxes[selectedIndex] = pxToBox(newBoxPx, currentBoxes[selectedIndex].class_id);
      render();
    }
  }
});

canvas.addEventListener("mouseup", (e) => {
  if (mode === "drawing") {
    const { x: mx, y: my } = getMousePos(e);
    const x1 = Math.min(drawStartX, mx);
    const y1 = Math.min(drawStartY, my);
    const boxW = Math.abs(mx - drawStartX);
    const boxH = Math.abs(my - drawStartY);

    if (boxW >= 5 && boxH >= 5) {
      const newBoxPx = { x: x1, y: y1, w: boxW, h: boxH };
      currentBoxes.push(pxToBox(newBoxPx, activeClassId));
      selectedIndex = currentBoxes.length - 1; // select the box you just drew
    }
  }

  mode = null;
  resizeHandle = null;
  dragOrigBox = null;
  render();
});

// ---- Save / navigate ----
async function saveCurrent() {
  const frameName = frames[currentIndex];
  await fetch(`/api/label/${frameName}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ boxes: currentBoxes }),
  });
  saveBtn.classList.add("saved");
  saveBtn.textContent = "Saved \u2713";
  refreshProgress();
}

async function goTo(index) {
  await saveCurrent();
  await loadFrame(index);
}

saveBtn.addEventListener("click", saveCurrent);
prevBtn.addEventListener("click", () => goTo(currentIndex - 1));
nextBtn.addEventListener("click", () => goTo(currentIndex + 1));

document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "SELECT") return;

  if (e.key >= "1" && e.key <= "9") {
    const idx = parseInt(e.key, 10) - 1;
    if (idx < classes.length) {
      activeClassId = idx;
      classSelect.value = idx;
    }
  } else if (e.key === "a" || e.key === "A" || e.key === "ArrowLeft") {
    goTo(currentIndex - 1);
  } else if (e.key === "d" || e.key === "D" || e.key === "ArrowRight") {
    goTo(currentIndex + 1);
  } else if (e.key === "s" || e.key === "S") {
    saveCurrent();
  } else if (e.key === "Backspace" || e.key === "Delete") {
    e.preventDefault();
    if (selectedIndex !== null) {
      // delete the currently selected box specifically
      currentBoxes.splice(selectedIndex, 1);
      selectedIndex = null;
      render();
    } else if (currentBoxes.length > 0) {
      // fallback: no selection -> remove the most recently drawn box
      currentBoxes.pop();
      render();
    }
  } else if (e.key === "Escape") {
    selectedIndex = null;
    render();
  }
});

window.addEventListener("resize", () => loadFrame(currentIndex));

init();
