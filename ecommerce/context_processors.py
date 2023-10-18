from cartapp.models import CartItem,WishlistItem

def carticon(request):
    try:
        cartitems = CartItem.objects.filter(currentuser=request.user)
        cartcount = cartitems.count()
    except:
        cartcount = 0
    return {'cartcount':cartcount}

def wishlisticon(request):
    try:
        wishlistitems = WishlistItem.objects.filter(currentuser=request.user)
        wishlistcount = wishlistitems.count()
    except:
        wishlistcount = 0

    return {'wishlistcount':wishlistcount}

        