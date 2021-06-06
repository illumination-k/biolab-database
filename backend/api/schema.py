from sqlalchemy.engine import interfaces
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from models import Primer as PrimerModel, User as UserModel


class UserBase:
    def __init__(self, username: str):
        super().__init__()
        self.username = username


class CreateUser(UserBase):
    def __init__(self, username: str, password: str):
        super().__init__(username)
        self.password = password


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


# class UserConnections(relay.Connection):
#     class Meta:
#         node = User


# class Primer(SQLAlchemyObjectType):
#     class Meta:
#         model = PrimerModel
#         interfaces = (relay.Node,)


# class PrimerConnections(relay.Connection):
#     class Meta:
#         node = Primer
