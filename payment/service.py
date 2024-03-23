from django.conf import settings
import requests
import json


class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    BASE_URL = "https://api.paystack.co/"

    # This method verifies a payment
    def verify_payment(self, ref, *args, **kwargs):
        path = f"transaction/verify/{ref}"

        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        url = self.BASE_URL + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data["status"], response_data["data"]

        response_data = response.json()
        return response_data["status"], response_data["message"]