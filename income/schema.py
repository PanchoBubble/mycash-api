from graphene import relay, ObjectType, String, List, Float
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

import graphene

from income.models import Income, IncomeType
from django.contrib.auth.models import User
from common.models import Stock, Currency

from .custom_filters import IncomeTypeFilter, IncomeFilter
from mycash.custom_graphene import CustomNode

class IncomeNode(DjangoObjectType):
    class Meta:
        model = Income
        interfaces = (CustomNode, )

class IncomeTypeNode(DjangoObjectType):
    class Meta:
        model = IncomeType
        interfaces = (CustomNode, )

class Query(ObjectType):
    income = relay.Node.Field(IncomeNode, id=String())
    def resolve_income(self, info, **kwargs):
        return Income.objects.get(pk=kwargs['id'])
    
    incomes = DjangoFilterConnectionField(IncomeNode, filterset_class=IncomeFilter)

    income_type = relay.Node.Field(IncomeTypeNode, id=String())
    def resolve_income_type(self, info, **kwargs):
        return IncomeType.objects.get(pk=kwargs['id'])
    
    income_types = DjangoFilterConnectionField(IncomeTypeNode, filterset_class=IncomeTypeFilter)

class CreateIncomeType(graphene.Mutation):
    income_type = relay.Node.Field(IncomeTypeNode)
    class Arguments:
        name = String()
        description = String()
    def mutate(self, info, name, description):
        income_type = IncomeType(name=name, description=description)
        income_type.save()
        return CreateIncomeType(income_type=income_type)

class EditIncomeType(graphene.Mutation):
    income_type = relay.Node.Field(IncomeTypeNode)
    class Arguments:
        id = String()
        name = String()
        description = String()
    def mutate(self, info, id, name, description):
        income_type = IncomeType.objecst.get(pk=id)
        income_type.name = name
        income_type.description = description
        income_type.save()
        return EditIncomeType(income_type=income_type)

class DeleteIncomeType(graphene.Mutation):
    confirmation = String()
    class Arguments:
        income_type_list = List(String)
    def mutate(self, info, income_type_list):
        for income_type_id in income_type_list:
            income_type = IncomeType.objects.get(pk=income_type_id)
            income_type.delete()
        return DeleteIncomeType(confirmation="Deletion Completed")

class CreateIncome(graphene.Mutation):
    income = relay.Node.Field(IncomeNode)
    class Arguments:
        amount = Float(required=True)
        date = String(required=True)
        description = String()
        type = String(required=True)
        owner = String(required=True)
        currency = String(required=True)

    def mutate(self, info, **inputs):
        _owner = User.objects.get(pk=inputs.get('owner'))
        _type = IncomeType.objects.get(pk=inputs.get('type'))
        _currency = Currency.objects.get(pk=inputs.get('currency'))
        income = Income(
            date=inputs.get('date'),
            description=inputs.get('description'),
            amount=inputs.get('amount'),
            owner=_owner,
            type=_type,
            currency=_currency
        )
        income.save()

        owner_stock, _ = Stock.objects.get_or_create(owner=_owner, currency=_currency)
        owner_stock.amount += inputs.get('amount')
        owner_stock.save()

        return CreateIncome(income=income)

class EditIncome(graphene.Mutation):
    income = relay.Node.Field(IncomeNode)
    class Arguments:
        id = String(required=True)
        amount = Float(required=True)
        date = String(required=True)
        description = String()
        type = String(required=True)
        owner = String(required=True)
        currency = String(required=True)

    def mutate(self, info, **inputs):
        _income = Income.objects.get(pk=inputs.get('id'))
        _type = IncomeType.objects.get(pk=inputs.get('type'))
        _owner = User.objects.get(pk=inputs.get('owner'))
        _currency = Currency.objects.get(pk=inputs.get('currency'))
        
        _income.owner = _owner
        _income.type = _type
        _income.currency = _currency
        _income.date = inputs.get('date')
        _income.description = inputs.get('description')

        _amount = inputs.get('amount')
        if _income.amount != float(_amount):
            owner_stock = Stock.objects.get(owner=_owner, currency=_currency)
            owner_stock.amount -= _income.amount
            owner_stock.amount += _amount
            owner_stock.save()

            _income.amount = _amount


        _income.save()
        return EditIncome(income=_income)

class DeleteIncome(graphene.Mutation):
    confirmation = String()
    class Arguments:
        income_list = List(String)
    def mutate(self, info, income_list):
        for income_id in income_list:
            income = Income.objects.get(pk=income_id)
            ownser_stock = Stock.objects.get(owner=income.owner, currency=income.currency)
            ownser_stock.amount -= income.amount
            ownser_stock.save()
            income.delete()
        return DeleteIncome(confirmation="Deletion Completed")

class Mutation(ObjectType):
    create_income = CreateIncome.Field()
    edit_income = EditIncome.Field()
    remove_incomes = DeleteIncome.Field()
    create_income_type = CreateIncomeType.Field()
    edit_income_type = EditIncomeType.Field()
    remove_incomes_type = DeleteIncomeType.Field()