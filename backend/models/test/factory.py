import factory
from factory.alchemy import SQLAlchemyModelFactory

from models import db_session
import models


class UserFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = models.User
    FACTORY_SESSION = db_session
