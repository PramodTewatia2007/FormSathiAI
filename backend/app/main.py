from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .config import FICTIONAL_DEMO_WARNING, BASE_DIR
from .api import demo, documents, qa, validation, session

app = FastAPI(
    title="FormSathiAI",
    description="Make complicated forms easier to understand. Fictional demo for scholarship and admission applications.",
    version="1.0.0"
)


@app.middleware("http")
async def prevent_api_response_caching(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    return response

# Include API Routers
app.include_router(demo.router)
app.include_router(documents.router)
app.include_router(qa.router)
app.include_router(validation.router)
app.include_router(session.router)


@app.get("/api/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": "FormSathiAI",
        "version": "1.0.0",
        "mode": "deterministic_offline_demo",
        "warning": FICTIONAL_DEMO_WARNING
    }


# Mount built frontend assets if dist folder exists
frontend_dist = BASE_DIR / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        # Don't turn unknown API paths into the frontend's index document.
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        root = frontend_dist.resolve()
        file_path = (root / full_path).resolve()
        if root in file_path.parents and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(root / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
