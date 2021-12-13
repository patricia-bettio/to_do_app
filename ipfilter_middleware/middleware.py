from django.core.exceptions import PermissionDenied
from django.conf import settings

class IPFilterMiddleware:
    def __init__(self, get_response):
        #this is called once, when the server starts
        self.get_response = get_response
        # One-time configuration and initialization.
    def __call__(self, request):
        #for testing:
        #allowed_ip_addresses = ['127.0.0.1']
        #but it's hardcoded, so we need to import it from settings actually
        allowed_ip_addresses = settings.IPFILTER_MIDDLEWARE['ALLOWED_IP_ADDRESSES']
        client_ip_address = request.META.get('REMOTE_ADDR')
        print(f'** client ip address: {client_ip_address}')

        if not client_ip_address in allowed_ip_addresses:
            raise PermissionDenied
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        response['X-IP-FILTER'] = 'IP FILTER BY KEA'
        return response
