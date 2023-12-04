from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics

from src.routes.routes import router
from src.utils.utils import lifespan

app = FastAPI(lifespan=lifespan, debug=True)  # TODO: remove debug after release
app.include_router(router=router)

instrumentator = Instrumentator().instrument(app).add(metrics.default()).expose(app)
