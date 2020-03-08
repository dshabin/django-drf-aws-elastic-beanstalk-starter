from django.core.serializers import serialize

def request_params_parser(requset , params):
    data = {}
    body_params_key = 'body_params'
    query_params_key = 'query_params'
    if params.get(body_params_key , None):
        for key in params.get(body_params_key , []) :
            if key in requset.data:
                data[key] = requset.data[key]
        for key in params.get(body_params_key , []) :
            if params.get(body_params_key)[key]['required']:
                if key not in data:
                    raise Exception('required:'+key)
    if params.get(query_params_key , None):
        for key in params.get(query_params_key , []) :
            if key in requset.query_params:
                data[key] = requset.query_params[key]
        for key in params.get(query_params_key , []) :
            if params.get(query_params_key)[key]['required']:
                if key not in data:
                    raise Exception('required:'+key)
    return data

