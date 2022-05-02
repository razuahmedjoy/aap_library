from .models import Main_Category,WebSettings

def header_context(request):
    try:
        categories = Main_Category.objects.all()
        web_settings = WebSettings.objects.last()
    except:
        categories = None
        web_settings = None
    context = {}
    context['categories'] = categories
    context['web_settings'] = web_settings
    return context