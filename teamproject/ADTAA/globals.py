from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# These decorators limit views to authenticated users (login_required) and ensures that Django won't cache the database
# queries because they need to be run for each request (never_cache)
# They will be used with the Views we define
VIEW_DECORATORS = [never_cache, login_required]


def raise_unexpected_error(error_instance):
    # If we hit an Exception that we don't expect, we need to figure out why we're hitting it.
    # Printing out the exception and its type can provide a good starting place for debugging
    print('Unexpected Error Encountered')
    print('Error Type: %s' % type(error_instance))
    print('Error:')
    print(error_instance)
    raise error_instance
