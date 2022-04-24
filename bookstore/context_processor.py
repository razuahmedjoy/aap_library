from .models import Main_Category

def header_context(request):
    try:
        categories = Main_Category.objects.all()
    except:
        categories = None
    context = {}
    context['categories'] = categories
    return context