
import json
import decimal
from rest_framework import generics, permissions, response, status, views
from .models import Payment
from rest_framework.response import Response
from .serializers import PaymentSerializer
from rest_framework.views import APIView
from core.serializers import JobSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveAPIView, ListAPIView,ListCreateAPIView,CreateAPIView


# Create your views here.
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Check if the transaction exists
        # try:
        #     transaction = PaymentSerializer.objects.get(paystack_reference=reference)
        #     return Response({'message': 'Transaction already processed'}, status=status.HTTP_200_OK)
        # except PaymentSerializer.DoesNotExist:
        #     pass
        
        # transaction_data = {
        #     'paystack_reference': reference,
        #     'amount':amount, # get amount from Paystack or frontend,
        #     'status': 'successful',
        #     # Add any other transaction details
        #     }
        
        payment_data = {
            'paystack_reference': request.data.get('paystack_reference'),
            'amount':request.data.get('amount'), # get amount from Paystack or frontend,
            'status': 'successful',
            # Add any other transaction details
            }

        job_data= {
            'job_type':request.data.get('job_type'),
            'city':request.data.get('city'), # get amount from Paystack or frontend,
            'street_adddress':request.data.get('street_adddress'),
            "job_description":request.data.get('job_description'),
            "time":request.data.get('time'),
            "completed":request.data.get('completed'),
            # Add any other transaction details
            }
        jobSerializer=JobSerializer(data=job_data, context={"userinfo":request.user})
        payment_serializer = PaymentSerializer(data=payment_data, context={"userinfo":request.user})
        if payment_serializer.is_valid() and  jobSerializer.is_valid():
            payment_serializer.save()
            jobSerializer.save()
            return Response({'message': 'Transaction recorded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    




















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

# class Webhook(generics.GenericAPIView):
#     """
#     This view handles updating wallet after payment has been made by user to fund the wallet
#     """
#     serializer_class = WebhookSerializer

#     def post(self, request, *args, **kwargs):
#         body = json.loads(request.body)
#         hash = hmac.new(bytes(settings.PAYSTACK_SECRET_KEY, 'utf-8'),
#                         str.encode(request.body.decode('utf-8')),
#                         digestmod=hashlib.sha512).hexdigest()
        
#         if request.META['HTTP_X_PAYSTACK_SIGNATURE'] == hash:
#             event = body['event']
#             data = body['data']
#             email = data['customer']['email']
#             if event == 'charge.success':
#                 user = User.objects.get(email=email)
#                 person = Person.objects.get(person=user)
#                 wallet = Wallet.objects.get(person=person)
#                 if data['status'] == 'success':
#                     BalanceAfter = wallet.balance + data["amount"]
#                     WalletTransaction.objects.create(wallet=wallet, type="AW", BalanceBefore=wallet.balance, BalanceAfter=BalanceAfter, amount=data["amount"])
#                     wallet.balance += decimal.Decimal(data["amount"]/100)
#                     wallet.save()
                    
#                     return response.Response(status=status.HTTP_200_OK)
#                 else:
#                     return response.Response(status=status.HTTP_400_BAD_REQUEST)
#         return response.Response(status=status.HTTP_400_BAD_REQUEST)




