import sys
from pathlib import Path

# Ensure project root is on sys.path so "import pageindex" works
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PageIndex Web", version="1.0.0")

# CORS for dev (Vite dev server on :3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
from server.routers import documents, chat, config as config_router
app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(config_router.router)

# Serve extracted document images (referenced from generated Markdown as
# ![](/media/<doc>/<file>.png)). Must be mounted before the catch-all static
# mount below so it takes precedence.
MEDIA_DIR = PROJECT_ROOT / "media"
MEDIA_DIR.mkdir(exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# Serve built frontend (production)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
