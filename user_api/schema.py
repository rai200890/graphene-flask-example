import re
import logging

import graphene
from graphql.error import GraphQLError
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType


from .models import User, Phone

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FilterQueryBuilder(object):

    def __init__(self, base_query, args):
        self.base_query = base_query
        self.args = args

    @property
    def entity(self):
        return self.base_query.column_descriptions[0]["entity"]

    def build(self):
        query = self.base_query
        for field_name, value in self.args.items():
            query = query.filter(self._build_filter_predicate(field_name, value))
        return query

    def _build_filter_predicate(self, name, value):
        field_name, insensitive_case, matcher = re.match(r"(.*)_(I?)(.*)", name).groups()
        field = getattr(self.entity, field_name.lower())
        operator = "like"
        if insensitive_case:
            operator = "ilike"
        matchers = {
            "startswith": "{}%",
            "endswith": "%{}",
            "contains": "%{}%",
            "exact": "{}"
        }
        template = matchers[matcher.lower()]
        return getattr(field, operator)(template.format(value))


class QueryResolver(object):

    def __init__(self, info, **args):
        self.info = info
        self.args = args

    @property
    def base_query(self):
        graphene_type = self.info.return_type.graphene_type
        if issubclass(graphene_type, relay.Connection):
            graphene_type = graphene_type.Edge.node.type
        base_query = graphene_type.get_query(self.info)
        return base_query

    @property
    def filter_args(self):
        return {key: value for key, value in self.args.items()
                if key not in ["first", "before", "after", "last"]}

    def resolve(self):
        query = FilterQueryBuilder(self.base_query, self.filter_args).build()
        return query


def resolve_query(root, info, **args):
    query = QueryResolver(info, **args).resolve()
    return query.all()


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
            raise GraphQLError(message=str(e))


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class UserQuery(graphene.ObjectType):
    user = relay.Node.Field(UserType)
    users = SQLAlchemyFilterConnectionField(UserConnection,
                                            name_Istartswith=graphene.String(name="name_Istartswith"))


schema = graphene.Schema(query=UserQuery, mutation=Mutation, types=[UserType, PhoneType])
