from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'transaction_id', 'amount', 'method', 'status', 'created_at']
        read_only_fields = ['id', 'transaction_id', 'status', 'created_at']  # These fields are set by the backend
