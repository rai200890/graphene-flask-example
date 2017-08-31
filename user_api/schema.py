import re

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import User, Phone


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


class NodeInterface(graphene.Interface):

    @classmethod
    def get_node(cls, info, id):
        node = cls._meta.model.query.get(id)
        return node


class UserType(SQLAlchemyObjectType, NodeInterface):
    class Meta:
        model = User
        interfaces = [relay.Node]


class UserConnection(graphene.Connection):
    class Meta:
        node = UserType


class PhoneType(SQLAlchemyObjectType, NodeInterface):
    class Meta:
        model = Phone
        interfaces = [relay.Node]


class SQLAlchemyFilterConnectionField(relay.ConnectionField):

    def __init__(self, connection, **fields):
        return super(SQLAlchemyFilterConnectionField, self).__init__(connection,
                                                                     resolver=resolve_query,
                                                                     **fields)


class Query(graphene.ObjectType):
    user = relay.Node.Field(UserType)
    users = SQLAlchemyFilterConnectionField(UserConnection,
                                            name_Istartswith=graphene.String(name="name_Istartswith"))


schema = graphene.Schema(query=Query)
