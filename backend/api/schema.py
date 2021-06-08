from sqlalchemy.engine import interfaces
import graphene
from graphql import GraphQLError
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from access_token import check_access_token
from models import Primer as PrimerModel, User as UserModel

import logging

logger = logging.getLogger(__name__)


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


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    allUsers = graphene.List(User, token=graphene.String())
    allPrimers = graphene.List(Primer, token=graphene.String())

    def resolve_allUsers(self, info, token: str):
        if check_access_token(token=token) is None:
            raise GraphQLError("Invalid credentials")

        # SQLarchemyのクエリオブジェクトが帰ってくるので、フィルタとかはそこからやればいい
        query = User.get_query(info)
        return query.all()

    def resolve_allPrimers(self, info, token: str):
        if check_access_token(token=token) is None:
            raise GraphQLError("Invalid credentials")

        query = Primer.get_query(info)
        return query.all()
