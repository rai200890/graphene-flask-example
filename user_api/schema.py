import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from user_api.models import User as UserModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel


class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, args, context, info):
        query = User.get_query(context)
        return query.all()


schema = graphene.Schema(query=Query)
