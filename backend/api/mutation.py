import bcrypt
import graphene
import crud
from api import schema
from graphql import GraphQLError
from typing import Optional
from jwt import PyJWTError

from access_token import create_access_token_with_username, check_access_token
from models import db_session

import logging

logger = logging.getLogger(__name__)

db = db_session.session_factory()


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, username: str, password: str):
        logger.debug(f"username: {username}, password: {password}")
        ok = True

        if crud.get_user_by_username(db, username) is not None:
            raise GraphQLError("Username already registered")

        user = schema.CreateUser(username=username, password=password)
        crud.create_user(db, user)
        return CreateUser(ok=ok)


class AuthenUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()

    @staticmethod
    def mutate(root, info, username: str, password: str):
        # get user info
        db_user = crud.get_user_by_username(db, username)
        if db_user is None:
            raise GraphQLError("Username not existed")
        # check password
        is_password_correct = crud.check_password(
            db=db, username=username, password=password
        )

        if not is_password_correct:
            raise GraphQLError("Password is not correct")

        access_token = create_access_token_with_username(username)

        return AuthenUser(token=access_token)


class CreateNewPrimer(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)
        name = graphene.String()
        desc = graphene.String()
        seq = graphene.String()

    token = graphene.String()

    @staticmethod
    def mutate(root, info, token: str, name: str, seq: str, desc: Optional[str] = None):
        user = check_access_token(token)

        if user is None:
            raise GraphQLError("Invalid credentials")

        primer = crud.create_primer(db=db, user=user, name=name, seq=seq)

        token = create_access_token_with_username(user.username)
        return CreateNewPrimer(token=token)
