from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock
from rest_framework.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['stock_id', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def validate_positions(self, value):
        all_product = Product.objects.all().values_list('pk', flat=True)
        for position in value:
            if int(position['product'].id) not in all_product:
                raise ValidationError(f'Продукта с id: {position["product"].id} не существует')
        return value

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(
                stock_id=stock.id,
                quantity=position['quantity'],
                price=position['price'],
                product=position['product']
            )

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for position in positions:
            product = position['product']
            quantity = position['quantity']
            price = position['price']
            StockProduct.objects.update_or_create(
                stock=stock,
                product=product,
                defaults={'quantity': quantity, 'price': price}
            )

        return stock