import graphene
import crud

from graphql import GraphQLError
from typing import Optional

from access_token import create_access_token_with_username, check_access_token
from models import db_session

import logging

logger = logging.getLogger(__name__)

db = db_session.session_factory()


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
