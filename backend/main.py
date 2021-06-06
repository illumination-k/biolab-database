import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from api import mutation, schema

### Set Log Level ###
import os
import logging
from colorful_handler import ColorfulHandler

_log_level = os.environ.get("LOGLEVEL")
if _log_level is None:
    log_level = logging.DEBUG
elif _log_level == "error":
    log_level = logging.ERROR
elif _log_level == "warning":
    log_level = logging.WARNING
elif _log_level == "warn":
    log_level = logging.WARN
elif _log_level == "info":
    log_level = logging.INFO

logging.basicConfig(handlers=[ColorfulHandler()], level=log_level)
logger = logging.getLogger(__name__)
#########################

backend = FastAPI()


class Mutations(graphene.ObjectType):
    createUser = mutation.CreateUser.Field()
    auth = mutation.AuthenUser.Field()
    createPrimer = mutation.CreatePrimer.Field()


backend.add_route(
    "/graphql",
    GraphQLApp(schema=graphene.Schema(query=schema.Query, mutation=Mutations)),
)


@backend.get("/")
def read_root():
    return {"Hello": "World"}
