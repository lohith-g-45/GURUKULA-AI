from .health import router as health_router
from .research import router as research_router
from .planning import router as planning_router
from .tasks import router as tasks_router
from .tasks import agent_router
from .user import router as user_router
from .dashboard import router as dashboard_router

__all__ = ["health_router", "research_router", "planning_router", "tasks_router", "agent_router", "user_router", "dashboard_router"]