from drf_yasg.utils import swagger_auto_schema

def add_swagger_tags(tags):
    """
    Dekorator koji dodaje tagove za sve metode ViewSet-a.
    """
    def decorator(viewset_class):
        methods = ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy']
        
        for method_name in methods:
            if hasattr(viewset_class, method_name):
                method = getattr(viewset_class, method_name)
                decorated_method = swagger_auto_schema(tags=tags)(method)
                setattr(viewset_class, method_name, decorated_method)

        return viewset_class

    return decorator
