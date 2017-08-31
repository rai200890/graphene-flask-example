from flask_graphql import GraphQLView


class UserGraphQLView(GraphQLView):

    # TODO: Improve error handling
    def dispatch_request(self):
        response = super(UserGraphQLView, self).dispatch_request()
        # if response.mimetype == "application/json":
        #     body = json.loads(response.data.decode("utf-8"))
        #     if any(body.get("errors", [])):
        #         if "IntegrityError" in body["errors"][0]["message"]:
        #             response.status_code = 400
        return response
