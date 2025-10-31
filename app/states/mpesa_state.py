import reflex as rx
import os
import requests
import base64
from datetime import datetime
import logging


class MpesaState(rx.State):
    """Handles M-Pesa payment integration."""

    is_processing: bool = False
    payment_status: str = ""
    error_message: str = ""
    phone_number: str = ""
    amount: float = 0.0

    def _get_access_token(self) -> str | None:
        consumer_key = os.getenv("MPESA_CONSUMER_KEY")
        consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
        if not consumer_key or not consumer_secret:
            self.error_message = "M-Pesa API credentials are not configured."
            logging.error(self.error_message)
            return None
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        try:
            response = requests.get(
                auth_url,
                auth=requests.auth.HTTPBasicAuth(consumer_key, consumer_secret),
            )
            response.raise_for_status()
            data = response.json()
            return data.get("access_token")
        except requests.exceptions.RequestException as e:
            self.error_message = f"Failed to get M-Pesa access token: {e}"
            logging.exception(f"Error: {e}")
            return None

    @rx.event
    def initiate_stk_push(self, phone: str, amount: float):
        self.is_processing = True
        self.payment_status = ""
        self.error_message = ""
        self.phone_number = phone
        self.amount = float(amount)
        access_token = self._get_access_token()
        if not access_token:
            self.is_processing = False
            return
        business_shortcode = os.getenv("MPESA_BUSINESS_SHORTCODE")
        passkey = os.getenv("MPESA_PASSKEY")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password_string = f"{business_shortcode}{passkey}{timestamp}"
        password = base64.b64encode(password_string.encode()).decode()
        stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(self.amount),
            "PartyA": self.phone_number,
            "PartyB": business_shortcode,
            "PhoneNumber": self.phone_number,
            "CallBackURL": "https://your-domain.com/api/mpesa_callback",
            "AccountReference": "WeighBridge-Txn",
            "TransactionDesc": "Payment for weighing service",
        }
        try:
            response = requests.post(stk_push_url, json=payload, headers=headers)
            response.raise_for_status()
            self.payment_status = "STK push initiated. Please check your phone."
            logging.info(f"M-Pesa STK push response: {response.json()}")
        except requests.exceptions.RequestException as e:
            self.error_message = f"Failed to initiate STK push: {e}"
            logging.exception(f"Error: {e}")
        finally:
            self.is_processing = False