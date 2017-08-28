import logging
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from user_api.models import User as UserModel, Phone as PhoneModel


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = [relay.Node]


class Phone(SQLAlchemyObjectType):
    class Meta:
        model = PhoneModel
        interfaces = [relay.Node]


class Query(graphene.ObjectType):
    users = graphene.List(User, id=graphene.Int(), name=graphene.String())

    def resolve_users(self, args, context, info):
        query = User.get_query(context).filter_by(**args)
        return query.all()


schema = graphene.Schema(query=Query)
