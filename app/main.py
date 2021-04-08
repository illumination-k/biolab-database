import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

app = FastAPI()

class Query(graphene.ObjectType):
    # 引数nameを持つフィールドhelloを作成
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    # フィールドhelloに対するユーザへ返すクエリレスポンスを定義
    def resolve_hello(self, info, name: str):
        return "Hello " + name

app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))

@app.get("/")
def read_root():
    return {"Hello": "World"}