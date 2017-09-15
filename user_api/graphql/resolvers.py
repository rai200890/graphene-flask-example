import re

from graphene import relay


class PredicateParser(object):

    def __init__(self, predicate):
        field_name, insensitive_case, matcher = re.match(r"(.*)_(I?)(.*)", predicate).groups()
        self.insensitive_case = insensitive_case is None
        self.field_name = field_name.lower()
        self.matcher = matcher.lower()


class FilterPredicate(object):

    def __init__(self, entity, name, value):
        self.entity = entity
        self.name = name
        self.value = value

    @property
    def parser(self):
        return PredicateParser(self.name)

    @property
    def field(self):
        return getattr(self.entity, self.parser.field_name)

    @property
    def operator(self):
        operator = "like"
        if self.parser.insensitive_case:
            operator = "ilike"
        return operator

    @property
    def template(self):
        matchers = {
            "startswith": "{}%",
            "endswith": "%{}",
            "contains": "%{}%",
            "exact": "{}"
        }
        return matchers[self.parser.matcher]

    @property
    def predicate(self):
        return getattr(self.field, self.operator)(self.template.format(self.value))


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
            filter_predicate = FilterPredicate(self.entity, field_name, value)
            query = query.filter(filter_predicate.predicate)
        return query


class QueryResolver(object):

    def __init__(self, info, **args):
        self.info = info
        self.args = args

    @property
    def base_query(self):
        return self.graphene_type.get_query(self.info)

    @property
    def graphene_type(self):
        graphene_type = self.info.return_type.graphene_type
        if issubclass(graphene_type, relay.Connection):
            graphene_type = graphene_type.Edge.node.type
        return graphene_type

    @property
    def filter_args(self):
        return {key: value for key, value in self.args.items()
                if key not in ["first", "before", "after", "last"]}

    def resolve(self):
        return FilterQueryBuilder(self.base_query, self.filter_args).build()


def resolve_query(root, info, **args):
    query = QueryResolver(info, **args).resolve()
    return query.all()
