
from rest_framework import serializers
from apps_.users.models import Taker
from .models import Payment
from apps_.orders.models import TopshirishPunktlar


class PaymentCreateSerializer(serializers.Serializer):
	order_id = serializers.IntegerField()
	provider = serializers.ChoiceField(choices=Payment.PaymentProvider.choices)

	def validate_order_id(self, value):
		from apps_.orders.models import Order
		try:
			order = Order.objects.get(pk=value)
		except Order.DoesNotExist:
			raise serializers.ValidationError("Order not found")
		return value


class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = [
			'id', 'order', 'amount', 'currency', 'provider', 'provider_payment_id', 'status', 'created_at', 'updated_at'
		]


class TopshirishPunktSerializer(serializers.Serializer):
    class Meta:
        model = TopshirishPunktlar
        fields = ['id', 'viloyat', 'tuman_or_shahar', 'kucha', 'uy_raqami','xonodon', 'pades', 'qavat']
        
    

class TakerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Taker
		fields = ('name', 'surname', 'phone')

class PromotionSerializer(serializers.Serializer):
	code = serializers.CharField(required=True)
 
 