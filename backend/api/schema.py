from sqlalchemy.engine import interfaces
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from ..models import Primer as PrimerModel, User as UserModel


class UserBase:
    username: str


class CreateUser(UserBase):
    password: str


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class UserConnections(relay.Connection):
    class Meta:
        node = User


class Primer(SQLAlchemyObjectType):
    class Meta:
        model = PrimerModel
        interfaces = (relay.Node,)


class PrimerConnections(relay.Connection):
    class Meta:
        node = Primer
