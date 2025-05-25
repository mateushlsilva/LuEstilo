from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
from app.config import settings
from app.routers import authRouter, clienteRouter, produtoRouter, pedidoRouter, whatsappRouter


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

app.include_router(authRouter.router)
app.include_router(clienteRouter.router)
app.include_router(produtoRouter.router)
app.include_router(pedidoRouter.router)
#app.include_router(whatsappRouter.router)
