# https://stackoverflow.com/questions/63629935/django-3-1-and-is-ajax

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
