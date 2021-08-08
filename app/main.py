from fastapi import FastAPI

from containers import Container
import endpoints


def create_app() -> FastAPI:
    container = Container()
    # To make the injection work we need to wire the container instance with the endpoints module. This needs to be done once.
    container.wire(modules=[endpoints])

    db = container.db()
    # For create all tables
    # If you created them before, you can comment this line
    db.create_database()

    app = FastAPI()
    # FastAPI app provide container property as default
    app.container = container

    # Simply add router endpoints
    app.include_router(endpoints.router)
    return app


app = create_app()
