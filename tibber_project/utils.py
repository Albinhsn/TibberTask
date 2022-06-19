


from json import loads

def parse_body_from_request(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    return body


