from commons.helpers import queryset_to_python_dict

def user_serializer(user):
    data = queryset_to_python_dict([user],many=False)
    data.pop('password')
    return data

def users_serializer(user_queryset):
    data = []
    for user in user_queryset:
        data.append(user_serializer(user))
    return data