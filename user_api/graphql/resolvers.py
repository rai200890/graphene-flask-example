import re

from graphene import relay


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
        return FilterQueryBuilder(self.base_query, self.filter_args).build()


def resolve_query(root, info, **args):
    query = QueryResolver(info, **args).resolve()
    return query.all()
