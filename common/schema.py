from graphene_django import DjangoObjectType
from graphene import relay, ObjectType, String, List, Float 
from graphene_django.filter import DjangoFilterConnectionField
import graphene

from django.contrib.auth.models import User
from common.models import Currency, Stock

from .custom_filters import CurrencyFilter, StockFilter
from mycash.custom_graphene import CustomNode

class StockeNode(DjangoObjectType):
    class Meta:
        model = Stock
        interfaces = (CustomNode, )

class CurrencyNode(DjangoObjectType):
    class Meta:
        model = Currency
        interfaces = (CustomNode, )

class Query(ObjectType):
    stock = relay.Node.Field(StockeNode, id=String())
    def resolve_stock(self, info, **kwargs):
        return Stock.objects.get(pk=kwargs['id'])
    
    stocks = DjangoFilterConnectionField(StockeNode, filterset_class=StockFilter)

    currency = relay.Node.Field(CurrencyNode, id=String())
    def resolve_expense_type(self, info, **kwargs):
        return Currency.objects.get(pk=kwargs['id'])
    
    currencies = DjangoFilterConnectionField(CurrencyNode, filterset_class=CurrencyFilter)

class CreateStock(graphene.Mutation):
    stock = relay.Node.Field(StockeNode)
    class Arguments:
        currency = String(required=True)
        owner = String()
        amount = Float()

    def mutate(self, info, **inputs):
        _owner = User.objects.get(username=inputs.get('owner'))
        _currency = Currency.objects.get(pk=inputs.get('currency'))
        stock = Stock(
            amount=inputs.get('amount'),
            owner=_owner,
            currency=_currency
        )
        stock.save()
        return CreateStock(stock=stock)

class EditStock(graphene.Mutation):
    stock = relay.Node.Field(StockeNode)
    class Arguments:
        id = String(required=True)
        currency = String(required=True)
        owner = String()
        amount = Float()

    def mutate(self, info, **inputs):
        _stock = Stock.objects.get(pk=inputs.get('id'))
        _currency = Currency.objects.get(pk=inputs.get('currency'))
        _owner = User.objects.get(username=inputs.get('owner'))

        _stock.owner = _owner
        _stock.currency = _currency
        _stock.amount = inputs.get('amount')
        _stock.save()
        return EditStock(stock=_stock)

class DeleteStock(graphene.Mutation):
    confirmation = String()
    class Arguments:
        stock_list = List(String)
    def mutate(self, info, stock_list):
        for stock_id in stock_list:
            stock = Stock.objects.get(pk=stock_id)
            stock.delete()
        return DeleteStock(confirmation="Deletion Completed")

class CreateCurrency(graphene.Mutation):
    currency = relay.Node.Field(CurrencyNode)
    class Arguments:
        name = String()
        code = String()
    def mutate(self, info, name, code):
        currency = Currency(name=name, code=code)
        currency.save()
        return CreateCurrency(currency=currency)

class EditCurrency(graphene.Mutation):
    currency = relay.Node.Field(CurrencyNode)
    class Arguments:
        id = String()
        name = String()
        code = String()
    def mutate(self, info, id, name, code):
        currency = Currency.objecst.get(pk=id)
        currency.name = name
        currency.code = code
        currency.save()
        return EditCurrency(currency=currency)

class DeleteCurrency(graphene.Mutation):
    confirmation = String()
    class Arguments:
        currency_list = List(String)
    def mutate(self, info, currency_list):
        for currency_id in currency_list:
            currency = Currency.objects.get(pk=currency_id)
            currency.delete()
        return DeleteCurrency(confirmation="Deletion Completed")

class Mutation(ObjectType):
    create_stock = CreateStock.Field()
    edit_stock = EditStock.Field()
    remove_stock = DeleteStock.Field()
    create_currency = CreateCurrency.Field()
    edit_currency = EditCurrency.Field()
    remove_currency = DeleteCurrency.Field()