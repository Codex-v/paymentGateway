from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .ccavutil import decrypt,encrypt
from string import Template
from django.conf import settings as s
from django.http import JsonResponse
from .utils import Utils


accessCode = s.CC_ACCESS_CODE
workingKey =  s.CC_WORKING_KEY

@api_view(['GET'])
def webprint(request,orderid):
    data = Utils.getCustomrData(orderid)
    if data == None:
        return JsonResponse({'message':'payment is done for this order id'})    
    return render(request, 'dataFrom.htm',{'data': data})


@api_view(['POST'])
def ccavResponseHandler(request):
    Utils.res(request.POST.get('encResp', ''))
    

@api_view(['POST'])
def ccavRequestHandler(request):
        form_data = {
            'merchant_id':2924061,
            'order_id': request.POST.get('order_id',''),
            'order_id': request.POST.get('order_id',''),
            'currency':request.POST.get('currency'),
            'amount' : request.POST.get('amount'),
            'redirect_url' : 'http://192.168.1.21:8505/payment/ccavResponseHandler/',
            'cancel_url' : 'https://awakenmindmaps.com/cancle.html',
            'language' : 'en',
            'billing_name' : request.POST.get('biller_name',''),
            'billing_email' : request.POST.get('biller_email',''),
            'billing_tel' : request.POST.get('biller_tel',''),
        }

        # print(form_data)
        merchant_data = '&'.join([f'{key}={value}' for key, value in form_data.items()])
        # print(merchant_data)
        print(merchant_data)
        
        encryption = encrypt(merchant_data, workingKey)
        # print(encryption)

        
        html_template = '''
        <html>
        <head>
            <title>Sub-merchant checkout page</title>
            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        </head>
        <body>
            <form id="nonseamless" method="post" name="redirect" action="https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction">
                <input type="hidden" id="encRequest" name="encRequest" value="$encReq">
                <input type="hidden" name="access_code" id="access_code" value="$xscode">
                <script language='javascript'>document.redirect.submit();</script>
            </form>
        </body>
        </html>
        '''

        html_content = Template(html_template).safe_substitute(encReq=encryption, xscode=accessCode)

        return HttpResponse(html_content)

