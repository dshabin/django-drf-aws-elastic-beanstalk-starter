from django.core.serializers import serialize


def queryset_to_python_dict(queryset,many):
    res = []
    python_dicts_array = serialize('python' , queryset)
    for obj in python_dicts_array:
        temp = {}
        temp = obj['fields']
        temp['id'] = obj['pk']
        res.append(temp)
    if many:
        return res
    else:
        return res[0]
