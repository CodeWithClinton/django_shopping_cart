from .models import *


def cart_renderer(request):
    
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, completed=False)
            
        else:
            cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
            
    except:
        cart = {"num_of_items":0}
            
    return {"cart": cart}




