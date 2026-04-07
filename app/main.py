from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.database import init_db
from app.api import auth, customers, payments, dashboard
from app.api import reminders as reminders_api
from app.reminders import start_reminder_service, stop_reminder_service
from app.twilio_service import twilio_service  # Initialize Twilio on startup

# Create FastAPI app
app = FastAPI(
    title="Vaishnavi Silk - Payment Reminder System",
    description="A simple payment tracking and reminder system for Vaishnavi Silk | Powered by CM",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(customers.router, prefix="/api")
app.include_router(payments.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(reminders_api.router, prefix="/api")

# Mount static files
static_path = Path(__file__).parent.parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized")
    # Uncomment the line below to enable automatic reminders
    # start_reminder_service()
    print("🚀 Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    # Uncomment if reminder service is enabled
    # stop_reminder_service()
    print("👋 Application shutdown")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    html_file = Path(__file__).parent.parent / "static" / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    return HTMLResponse(content="<h1>Payment Reminder Tool</h1><p>Frontend not found. Please check static folder.</p>")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Payment Reminder Tool is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
