import hashlib, hmac, requests
import json
import decimal
from rest_framework import generics, permissions, response, status, views
from wallet.models import Wallet
from .serializers import WebhookSerializer, WalletSerializer, TransactionSerializer
from .models import Wallet, WalletTransaction
from accounts.models import Person, User
from core import settings
from crowdfunding_api.permissions import PersonPermission
import requests

# Create your views here.
'''class VerifyPayment(views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            reference = request.query_params['reference']
            print(reference)
            r = requests.get(f"https://api.body.co/transaction/verify/:{reference}", headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"})  
            if r.status == "true":
                if r.data.status == 'success':
                    wallet = Wallet.objects.get(email=r.data.customer.email)
                    BalanceAfter = wallet.balance + r.data.amount
                    WalletTransaction.objects.create(wallet=wallet, type="AW", BalanceBefore=wallet.balance, BalanceAfter=BalanceAfter, amount=r.data.amount)
                    wallet.balance += r.data.amount
                    wallet.save()
                    
                    return response.Response("Your Wallet has been Updated", status=status.HTTP_200_OK)                   
            return response.Response("Unable to fund wallet", status=status.HTTP_400_BAD_REQUEST)
        except:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
'''

class Webhook(generics.GenericAPIView):
    """
    This view handles updating wallet after payment has been made by user to fund the wallet
    """
    serializer_class = WebhookSerializer

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        hash = hmac.new(bytes(settings.PAYSTACK_SECRET_KEY, 'utf-8'),
                        str.encode(request.body.decode('utf-8')),
                        digestmod=hashlib.sha512).hexdigest()
        
        if request.META['HTTP_X_PAYSTACK_SIGNATURE'] == hash:
            event = body['event']
            data = body['data']
            email = data['customer']['email']
            if event == 'charge.success':
                user = User.objects.get(email=email)
                person = Person.objects.get(person=user)
                wallet = Wallet.objects.get(person=person)
                if data['status'] == 'success':
                    BalanceAfter = wallet.balance + data["amount"]
                    WalletTransaction.objects.create(wallet=wallet, type="AW", BalanceBefore=wallet.balance, BalanceAfter=BalanceAfter, amount=data["amount"])
                    wallet.balance += decimal.Decimal(data["amount"]/100)
                    wallet.save()
                    
                    return response.Response(status=status.HTTP_200_OK)
                else:
                    return response.Response(status=status.HTTP_400_BAD_REQUEST)
        return response.Response(status=status.HTTP_400_BAD_REQUEST)




