from django.http import HttpRequest
from django.contrib import messages

from time import time


time_between_requests = 10

def throttling_middleware(get_response):

    def middleware(request: HttpRequest):
        time_now = time()
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            previous_response_time = {
                ip: time(),
            }
            if time_now - previous_response_time[ip] < time_between_requests:
                messages.error(request, f'Max limit to request is {time_between_requests} seconds')
                response = get_response(request)
                return response
        response = get_response(request)
        return response

    return middleware