from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

# class MenuItemSerializer(serializers.ModelSerializer):
#     category_id = serializers.IntegerField(write_only=True)
#     category = CategorySerializer(read_only=True)
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()




class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    #stock = serializers.IntegerField(source='inventory')
    #price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta: 
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        extra_kwargs = {
            'price': {'min_value': 2},
            'stock': {'source': 'inventory', 'min_value': 0},
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=MenuItem.objects.all()
                    )
                ]
            }
        #validators = [
        #   UniqueTogetherValidator(
        #       queryset=MenuItem.objects.all(),
        #       fields=['title', 'price']
        #   ),
        # ]
        }

    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
    
    # def validate_price(self, price):
    #     if (value < 2):
    #         raise serializers.ValidationError('Price should not be less than 2.0')