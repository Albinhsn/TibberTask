from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from utils import calculate_result, parse_body_from_request
from time import time
@csrf_exempt
def enter_path(request):
    if request.method != "POST":
        return HttpResponseNotFound("")
    #get content from body
    body = parse_body_from_request(request)
    #calc result 
    start_time = time()
    result = calculate_result(body['start'], body['commands'])
    end_time = time() - start_time
    #insert into db
    #INSERT INTO executions values(datetime.now(), len(body['commands']), result,    end_time)
    #return record 
    return HttpResponse(f"it took {end_time} to calc and result was {result}")
