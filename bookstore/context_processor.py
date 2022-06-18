from .models import Main_Category,WebSettings, Customers, Cart

def header_context(request):

    # showing guest cart information
    try:   
        device = request.COOKIES['device']
    except:
        device = []
    customer, created = Customers.objects.get_or_create(device=device, name="guest-auto")
    cart = Cart.objects.filter(user=customer)
    cart_len = len(cart)


    try:
        categories = Main_Category.objects.all()
        web_settings = WebSettings.objects.last()
    except:
        categories = None
        web_settings = None
    context = {}
    context['categories'] = categories
    context['web_settings'] = web_settings
    context['guest_cart'] = cart_len
    return context