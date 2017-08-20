
def students_proc(request):
    portal_url = request.scheme + '://' + request.META["HTTP_HOST"]
    return {'PORTAL_URL': portal_url}
