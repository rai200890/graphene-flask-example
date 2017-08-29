import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from user_api.models import User, Phone


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = [relay.Node]
    #
    # @classmethod
    # def get_node(cls, info, id):
    #     node = User.query.get(id)
    #     return node


class PhoneType(SQLAlchemyObjectType):
    class Meta:
        model = Phone
        interfaces = [relay.Node]

    @classmethod
    def get_node(cls, info, id):
        node = Phone.query.get(id)
        return node


class Query(graphene.ObjectType):
    users = graphene.List(UserType, id=graphene.Int(), name=graphene.String())

    def resolve_users(self, info, **args):
        query = UserType.get_query(info).filter_by(**args)
        result = query.all()
        return result


schema = graphene.Schema(query=Query)
