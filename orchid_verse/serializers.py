from rest_framework import serializers
from .models import OrchidPurchase

class OrchidPurchaseSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.name', read_only=True)

    class Meta:
        model = OrchidPurchase
        fields = [field.name for field in OrchidPurchase._meta.fields] + ['seller_name']
