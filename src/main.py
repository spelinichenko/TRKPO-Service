from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics

from src.routes.routes import router

app = FastAPI(debug=True)  # TODO: remove debug after release
app.include_router(router=router)

instrumentator = Instrumentator().instrument(app).add(metrics.default()).expose(app)
