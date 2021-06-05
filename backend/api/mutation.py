import bcrypt
import graphene
import crud
from api import schema
from graphql import GraphQLError
from models import db_session

db = db_session.session_factory()


class CreateUser(graphene.Mutation):
    class Argument:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, username: str, password: str):
        ok = True

        if crud.get_user_by_username(db, username) is not None:
            raise GraphQLError("Username already registered")

        user = schema.CreateUser(username=username, password=password)
        crud.create_user(db, user)
        return CreateUser(ok=ok)


class AuthenUser(graphene.Mutation):
    class Argument:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()

    @staticmethod
    def mutate(root, info, username: str, password: str):
        # get user info
        # check password
        pass
