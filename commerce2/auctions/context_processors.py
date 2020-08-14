from .models import Category


def categories(request):
    #categories = category.objects.values_list("category", flat=True)
    return {
        'categories': Category.objects.all()
    }