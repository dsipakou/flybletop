from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from .models import Product


class ProductResource(ModelResource):

    class Meta:
        queryset = Product.objects.all()
        filtering = {
            "type": ('exact'),
        }
        resource_name = 'product'
        serializer = Serializer(formats=['json'])

    def alter_list_data_to_serialize(self, request, data):
        return data['objects']


class ProductDetailsResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        filtering = {
            "slug": ('exact'),
        }
        resource_name = 'details'
        serializer = Serializer(formats=['json'])

    def alter_list_data_to_serialize(self, request, data):
        return data['objects']