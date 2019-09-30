import graphene
import graphql_jwt

import user.schema

class Query(user.schema.Query,
            graphene.ObjectType):
    pass


class Mutation( user.schema.Mutation,   
                graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

class PublicMutations(graphene.ObjectType):
    token_auth    = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token  = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()
    
public_schema = graphene.Schema(mutation=PublicMutations)
