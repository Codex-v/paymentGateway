from django.shortcuts import get_object_or_404
from django.conf import settings as setk
from api.models import *
from .ccavutil import decrypt
from urllib.parse import parse_qs


class Utils:
    @staticmethod
    def getCustomrData(orderid):
        CustomerData = get_object_or_404(AppointmentBooking,order_id=str(orderid))
        if CustomerData.status == "SUCCESS":
            return None
        form_data = {
            'biller_name':CustomerData.user.first_name,
            'biller_email':CustomerData.user.email,
            'order_id':orderid,
            'amount':CustomerData.price,
            'biller_tel':CustomerData.user.mobile_no
        }
        return form_data

    @staticmethod
    def res(encResp):
        print("called res")
        decResp = decrypt(encResp,setk.CC_WORKING_KEY)
        responseData = decResp
        parsedData = parse_qs(responseData)

        payment_ResponseData = {
            'order_id':parsedData.get('order_id',[None])[0],
            'tracking_id':parsedData.get('tracking_id',[None])[0],
            'bank_ref_no':parsedData.get('bank_ref_no',[None])[0],
            'order_status':str(parsedData.get('order_status',[None])[0]).upper(),
            'failure_message':parsedData.get('failure_message',[None])[0],
            'payment_mode':parsedData.get('payment_mode',[None])[0],
            'card_name':parsedData.get('card_name',[None])[0],
            'status_code':parsedData.get('status_code',[None])[0],
            'currency':parsedData.get('currency',[None])[0],
            'amount':parsedData.get('amount',[None])[0],
            'billing_name':parsedData.get('billing_name',[None])[0],
            'billing_tel':parsedData.get('billing_tel',[None])[0],
            'trans_date':parsedData.get('trans_date',[None])[0]
        }
        AppointmentBooking.objects.filter(order_id=payment_ResponseData['order_id']).update(status=payment_ResponseData['order_status'],payment_mode=payment_ResponseData['payment_mode'],payment_datetime=payment_ResponseData['trans_date'],payment_id=payment_ResponseData['tracking_id'])

        
    

   