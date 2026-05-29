from fastapi import FastAPI, APIRouter
from app.config import settings
from app.middleware import RequestLoggingMiddleware
from app.utils import logger, AppException, app_exception_handler, general_exception_handler
from app.routes import health_router, research_router, planning_router, tasks_router, agent_router, user_router, dashboard_router
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="GURUKULA AI Backend API",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(RequestLoggingMiddleware)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

api_router = APIRouter(prefix=settings.API_PREFIX)
api_router.include_router(health_router)
api_router.include_router(research_router)
api_router.include_router(planning_router)
api_router.include_router(tasks_router)
api_router.include_router(agent_router)
api_router.include_router(user_router)
api_router.include_router(dashboard_router)

app.include_router(api_router)

logger.info(f"Starting {settings.PROJECT_NAME} backend...")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
