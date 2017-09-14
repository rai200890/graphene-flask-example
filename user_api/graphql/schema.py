import logging

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from .resolvers import resolve_query
from ..models import User, Phone

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class UserType(SQLAlchemyObjectType):

    class Meta:
        model = User
        interfaces = [relay.Node]


class UserConnection(graphene.Connection):
    class Meta:
        node = UserType


class PhoneType(SQLAlchemyObjectType):
    class Meta:
        model = Phone
        interfaces = [relay.Node]


class SQLAlchemyFilterConnectionField(relay.ConnectionField):

    def __init__(self, connection, **fields):
        return super(SQLAlchemyFilterConnectionField, self).__init__(connection,
                                                                     resolver=resolve_query,
                                                                     **fields)


class PhoneInput(graphene.InputObjectType):
    ddd = graphene.String(required=True)
    number = graphene.String(required=True)


class CreateUser(relay.ClientIDMutation):

    class Input:
        name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        phones = graphene.List(PhoneInput)

    user = graphene.Field(UserType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            user = User.create(**input)
            logger.info("User {} created successfully".format(user.id))
            return CreateUser(user=user)
        except Exception as e:
            logger.error(e)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class UserQuery(graphene.ObjectType):
    user = relay.Node.Field(UserType)
    users = SQLAlchemyFilterConnectionField(UserConnection,
                                            name_Istartswith=graphene.String(name="name_Istartswith"))


schema = graphene.Schema(query=UserQuery, mutation=Mutation, types=[UserType, PhoneType])
