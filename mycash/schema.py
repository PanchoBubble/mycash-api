import graphene
import graphql_jwt

import user.schema
import income.schema
import expense.schema
import common.schema

class Query(user.schema.Query,
            income.schema.Query,
            expense.schema.Query,
            common.schema.Query,
            graphene.ObjectType):
    pass


class Mutation( user.schema.Mutation,   
                income.schema.Mutation,
                expense.schema.Mutation,
                common.schema.Mutation,
                graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

class PublicMutations(graphene.ObjectType):
    token_auth    = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token  = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()
    
public_schema = graphene.Schema(mutation=PublicMutations)
