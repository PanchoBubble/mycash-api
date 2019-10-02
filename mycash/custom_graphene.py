import graphene
from graphql_relay import to_global_id, from_global_id

class CustomNode(graphene.Node):
    class Meta:
        name = 'CustomNode'

    @classmethod
    def get_node_from_global_id(cls, info, global_id, only_type=None):
        node = super().get_node_from_global_id(global_id, info, only_type)
        if node:
            return node

        get_node = getattr(only_type, 'get_node', None)
        if get_node:
            return get_node(global_id, info)

    @classmethod
    def from_global_id(cls, type, id):
        return from_global_id(type, id)
    @classmethod
    def to_global_id(cls, type, id):
        return  id
