from graphene_django import DjangoObjectType
from graphene import relay, ObjectType, String, List, Float
from graphene_django.filter import DjangoFilterConnectionField
import graphene

from expense.models import Expense, ExpenseType
from django.contrib.auth.models import User
from common.models import Currency, Stock

from .custom_filters import ExpenseFilter, ExpenseTypeFilter
from mycash.custom_graphene import CustomNode

class ExpenseNode(DjangoObjectType):
    class Meta:
        model = Expense
        interfaces = (CustomNode, )

class ExpenseTypeNode(DjangoObjectType):
    class Meta:
        model = ExpenseType
        interfaces = (CustomNode, )

class Query(ObjectType):
    expense = relay.Node.Field(ExpenseNode, id=String())
    def resolve_expense(self, info, **kwargs):
        return Expense.objects.get(pk=kwargs['id'])
    
    expenses = DjangoFilterConnectionField(ExpenseNode, filterset_class=ExpenseFilter)

    expense_type = relay.Node.Field(ExpenseTypeNode, id=String())
    def resolve_expense_type(self, info, **kwargs):
        return Expense.objects.get(pk=kwargs['id'])
    
    expense_types = DjangoFilterConnectionField(ExpenseTypeNode, filterset_class=ExpenseTypeFilter)

class CreateExpense(graphene.Mutation):
    expense = relay.Node.Field(ExpenseNode)
    class Arguments:
        cost = Float(required=True)
        date = String()
        description = String()
        type = String(required=True)
        owner = String(required=True)
        state = String()
        currency = String(required=True)

    def mutate(self, info, **inputs):
        _owner = User.objects.get(username=inputs.get('owner'))
        _type = ExpenseType.objects.get(pk=inputs.get('type'))
        _currency = Currency.objects.get(pk=inputs.get('currency'))
        expense = Expense(
            date=inputs.get('date'),
            description=inputs.get('description'),
            state=inputs.get('state'),
            cost=inputs.get('cost'),
            owner=_owner,
            type=_type,
            currency=_currency
        )
        expense.save()

        if expense.state == 'Paid':
            owner_stock, _ = Stock.objects.get_or_create(owner=_owner, currency=_currency)
            owner_stock.amount -= inputs.get('cost')
            owner_stock.save()

        return CreateExpense(expense=expense)

class EditExpense(graphene.Mutation):
    expense = relay.Node.Field(ExpenseNode)
    class Arguments:
        id = String(required=True)
        cost = Float(required=True)
        date = String()
        description = String()
        type = String(required=True)
        owner = String(required=True)
        state = String()
        currency = String(required=True)

    def mutate(self, info, **inputs):
        _expense = Income.objects.get(pk=inputs.get('id'))
        _type = ExpenseType.objects.get(name=inputs.get('type'))
        _currency = Currency.objects.get(pk=inputs.get('currency'))
        _owner = User.objects.get(username=inputs.get('owner'))
        
        _expense.owner = _owner
        _expense.type = _type
        _expense.currency = _currency
        _expense.date = inputs.get('date')
        _expense.state = inputs.get('state')
        _expense.description = inputs.get('description')
        _cost = inputs.get('cost')

        if _expense.cost != float(_cost):
            if _expense.state == 'Paid':
                owner_stock = Stock.objects.get(owner=_owner, currency=_currency)
                owner_stock.amount -= _expense.cost
                owner_stock.amount += _cost
            owner_stock.save()

            _expense.cost = _cost
        _expense.cost = inputs.get('cost')

        _expense.save()
        return EditExpense(expense=_expense)

class DeleteExpense(graphene.Mutation):
    confirmation = String()
    class Arguments:
        expense_list = List(String)
    def mutate(self, info, expense_list):
        for expense_id in expense_list:
            expense = Expense.objects.get(pk=expense_id)
            if expense.state == 'Paid':
                ownser_stock = Stock.objects.get(owner=expense.owner, currency=expense.currency)
                ownser_stock.amount += expense.amount
                ownser_stock.save()
            expense.delete()
        return DeleteExpense(confirmation="Deletion Completed")

class CreateExpenseType(graphene.Mutation):
    expense_type = relay.Node.Field(ExpenseTypeNode)
    class Arguments:
        name = String()
        description = String()
    def mutate(self, info, name, description):
        expense_type = ExpenseType(name=name, description=description)
        expense_type.save()
        return CreateExpenseType(expense_type=expense_type)

class EditExpenseType(graphene.Mutation):
    expense_type = relay.Node.Field(ExpenseTypeNode)
    class Arguments:
        id = String()
        name = String()
        description = String()
    def mutate(self, info, id, name, description):
        expense_type = ExpenseType.objecst.get(pk=id)
        expense_type.name = name
        expense_type.description = description
        expense_type.save()
        return EditExpenseType(expense_type=expense_type)

class DeleteExpenseType(graphene.Mutation):
    confirmation = String()
    class Arguments:
        expense_type_list = List(String)
    def mutate(self, info, expense_type_list):
        for expense_type_id in expense_type_list:
            expense_type = ExpenseType.objects.get(pk=expense_type_id)
            expense_type.delete()
        return DeleteExpenseType(confirmation="Deletion Completed")

class Mutation(ObjectType):
    create_expense = CreateExpense.Field()
    edit_expense = EditExpense.Field()
    remove_expense = DeleteExpense.Field()
    create_expense_type = CreateExpenseType.Field()
    edit_expense_type = EditExpenseType.Field()
    remove_expense_type = DeleteExpenseType.Field()