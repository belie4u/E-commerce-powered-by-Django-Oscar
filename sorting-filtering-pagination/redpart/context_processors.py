from django.urls import resolve

def oscar_shop_tagline(request):
    url_name= resolve(request.path_info).url_name
    return {"OSCAR_SHOP_TAGLINE":url_name}