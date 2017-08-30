import graphene

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType


from .models import User, Phone


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


class Query(graphene.ObjectType):
    user = relay.Node.Field(UserType)
    users = relay.ConnectionField(UserConnection,
                                  name=graphene.String(name="name_Istartswith"))

    def resolve_users(self, info, **args):
        query = UserType.get_query(info)
        filters = {key: value for key, value in args.items()
                   if key not in ["first", "before", "after", "last"]}
        for key, value in filters.items():
            field = getattr(User, key)
            predicate = field.ilike("{}%".format(value))
            query = query.filter(predicate)

        return query.all()


schema = graphene.Schema(query=Query)
