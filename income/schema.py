import graphene
from graphene_django import DjangoObjectType
from graphene import relay

from graphene_django.filter import DjangoFilterConnectionField
from income.models import Income, IncomeType

from django.contrib.auth.models import User
import datetime

class IncomeNode(DjangoObjectType):
    class Meta:
        model = Income
        interfaces = (relay.Node, )
        filter_fields = {
                'amount': ['exact', 'icontains', 'istartswith'],
                'date': ['exact', 'icontains', 'istartswith'],
                'description': ['exact', 'icontains', 'istartswith'],
                'type__name': ['exact', 'icontains', 'istartswith'],
                'owner__username': ['exact', 'icontains', 'istartswith'],
        }

class Query(graphene.ObjectType):
    income = relay.Node.Field(IncomeNode, id=graphene.String())
    def resolve_income(self, info, **kwargs):
        return Income.objects.get(pk=kwargs['id'])
    
    incomes = DjangoFilterConnectionField(IncomeNode)

class CreateIncome(graphene.Mutation):
    income = relay.Node.Field(IncomeNode)
    class Arguments:
        amount = graphene.String(required=True)
        date = graphene.String(required=True)
        description = graphene.String()
        type = graphene.String(required=True)
        owner = graphene.String(required=True)

    def mutate(self, info, amount, date, description, type, owner):
        _owner = User.objects.get(username=owner)
        _type = IncomeType.objects.get(name=type)
        income = Income(
            date=date,
            description=description,
            owner=_owner,
            type=_type,
        )
        income.save()
        return CreateIncome(income=income)

class EditIncome(graphene.Mutation):
    income = relay.Node.Field(IncomeNode)
    class Arguments:
        id = graphene.String(required=True)
        amount = graphene.String(required=True)
        date = graphene.String(required=True)
        description = graphene.String()
        type = graphene.String(required=True)
        owner = graphene.String(required=True)

    def mutate(self, info, id, amount, date, description, type, owner):
        _income = Income.objects.get(pk=id)
        _owner = User.objects.get(username=owner)
        _type = IncomeType.objects.get(name=type)
        
        _income.owner = _owner
        _income.type = _type
        _income.amount = amount
        _income.date = date

        _income.save()
        return EditIncome(income=_income)

class Mutation(graphene.ObjectType):
    create_income = CreateIncome.Field()
    edit_income = EditIncome.Field()