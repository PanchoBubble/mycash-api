from graphene_django import DjangoObjectType
from graphene import relay, ObjectType, String, List, Float 
from graphene_django.filter import DjangoFilterConnectionField
import graphene
from .custom_filters import UserFilter

from mycash.custom_graphene import CustomNode

from django.contrib.auth.models import User

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (CustomNode, )

class Query(graphene.ObjectType):
    user = relay.Node.Field(UserNode, id=String()) 
    def resolve_user(self, info, id):
        return User.objects.get(pk = id)
    users = DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserNode)
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class EditUser(graphene.Mutation):
    user = graphene.Field(UserNode)
    class Arguments:
        id = graphene.String()
        username = graphene.String()
        email = graphene.String()
    def mutate(self, info, id, username, email):
        user = User.objects.get(pk=id)
        user.username = username
        user.email = email
        user.save()
        return EditUser(user=user)

class ChangePassword(graphene.Mutation):
    user = graphene.Field(UserNode)
    class Arguments:
        id = graphene.String()
        password = graphene.String()
    def mutate(self, info, id, password):
        user = User.objects.get(pk=id)
        user.set_password(password)
        user.save()
        return ChangePassword(user=user)

class DeleteUser(graphene.Mutation):
    confirmation = graphene.String()
    class Arguments:
        user_list = graphene.List(graphene.String)
    def mutate(self, info, user_list):
        for user_id in user_list:
            user = User.objects.get(pk=user_id)
            user.delete()
        return DeleteUser(confimation = "Deletion Completed")

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    edit_user = EditUser.Field()
    change_password = ChangePassword.Field()
    delete_user = DeleteUser.Field()