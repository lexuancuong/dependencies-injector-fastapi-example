from dependency_injector import containers, providers

from database import Database
from repositories import UserRepository
from services import UserService
from config import DATABASE_URL

# This container class wires
# - example user service
# - user repository 
# - utility database class
class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    # The gem of dependency injector :)
    # Singleton Strict
    db = providers.Singleton(Database, db_url=DATABASE_URL)

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

# the container class help all components obey to dependency injection principle
# `All entities just depend on abstract class`

