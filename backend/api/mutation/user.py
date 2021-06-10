import graphene
import crud
from api import schema
from graphql import GraphQLError
from typing import Optional
from jwt import PyJWTError

from access_token import create_access_token_with_username, check_access_token
from models import db_session
from models.init_models import init_user

import logging

logger = logging.getLogger(__name__)

db = db_session.session_factory()


class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()

    @staticmethod
    def mutate(root, info, email: str, username: str, password: str):
        logger.debug(f"username: {username}, password: {password}")
        ok = True

        if crud.get_user_by_username(db, username) is not None:
            raise GraphQLError("Username already registered")

        user = init_user(username=username, password=password, email=email)
        crud.create_user(db, user)
        token = create_access_token_with_username(user.username)
        return CreateUser(token=token)


class AuthenUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String(required=True)

    token = graphene.String()
    username = graphene.String()

    @staticmethod
    def mutate(
        root,
        info,
        password: str,
        email: Optional[str] = None,
        username: Optional[str] = None,
    ):
        logger.debug(f"username: {username}, email: {email}, password: {password}")
        # get user info
        if email is not None:
            user = crud.get_user(db, key="email", query=email)
        elif username is not None:
            user = crud.get_user(db, key="username", query=username)
        else:
            raise GraphQLError("Username or Email Fields is need")

        if user is None:
            raise GraphQLError("Username not existed")
        # check password
        is_password_correct = crud.check_password(
            db=db, username=username, password=password
        )

        if is_password_correct is None:
            raise GraphQLError("Password is not correct")

        access_token = create_access_token_with_username(username)

        return AuthenUser(token=access_token, username=user.username)
