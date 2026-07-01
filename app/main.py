"""FastAPI application entrypoint."""

from app.bootstrap import ApplicationFactory

app = ApplicationFactory().create_app()
