from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import BASE_DIR, get_settings
from app.database import init_db
from app.routes import dashboard, home, model_performance, prediction, users


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Akıllı evlerde enerji tüketimini tahmin eden web tabanlı makine öğrenmesi sistemi.",
    version="1.0.0",
    debug=settings.debug,
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")

app.include_router(home.router)
app.include_router(users.router)
app.include_router(prediction.router)
app.include_router(dashboard.router)
app.include_router(model_performance.router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict:
    return {"durum": "çalışıyor", "uygulama": settings.app_name}
