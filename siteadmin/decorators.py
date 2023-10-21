from django.views.decorators.cache import cache_control

def never_cache(view_func):
    return cache_control(no_cache=True, must_revalidate=True)(view_func)
