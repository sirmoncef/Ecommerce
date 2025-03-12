from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
import requests
import json
from django.conf import settings

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # User must be logged in
def create_payment(request):
    """Create a payment request to Chargily API"""
    data = request.data
    amount = data.get("amount")
    method = data.get("method")  # "CIB" or "EDAHABIA"

    if method not in ["CIB", "EDAHABIA"]:
        return Response({"error": "Invalid payment method"}, status=400)

    # Prepare payment request to Chargily API
    headers = {
        "Authorization": f"Bearer {settings.CHARGILY_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "client": request.user.username,
        "client_email": request.user.email,
        "amount": amount,
        "invoice_number": f"INV-{request.user.id}-{Payment.objects.count() + 1}",
        "payment_method": method,
        "back_url": settings.CHARGILY_BACK_URL,
        "webhook_url": settings.CHARGILY_WEBHOOK_URL,
        "discount": 0,
    }

    response = requests.post("https://api.chargily.com/v2/invoices", headers=headers, json=payload)

    if response.status_code == 201:
        response_data = response.json()
        payment = Payment.objects.create(
            user=request.user,
            transaction_id=response_data["invoice"]["id"],
            amount=amount,
            method=method,
            status="pending",
        )

        serializer = PaymentSerializer(payment)  # Serialize the created payment
        return Response({"payment": serializer.data, "payment_url": response_data["checkout_url"]}, status=201)

    return Response({"error": "Payment request failed"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_list(request):
    """List all payments of the authenticated user"""
    payments = Payment.objects.filter(user=request.user)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_detail(request, transaction_id):
    """Get details of a specific payment"""
    try:
        payment = Payment.objects.get(transaction_id=transaction_id, user=request.user)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)


@api_view(['POST'])
def payment_webhook(request):
    """Handle webhook notifications from Chargily"""
    data = request.data
    transaction_id = data.get("invoice", {}).get("id")
    status = data.get("status")

    if not transaction_id:
        return Response({"error": "Invalid webhook data"}, status=400)

    try:
        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.status = status  # Update payment status
        payment.save()
        return Response({"message": "Payment status updated"}, status=200)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)
