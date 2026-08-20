from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Category, Product

DEFAULT_PER_PAGE = 4
PER_PAGE_OPTIONS = [2, 4, 8, 12]


def product_list(request):
    categories = Category.objects.all()
    category_slug = request.GET.get("category")

    try:
        per_page = int(request.GET.get("per_page", DEFAULT_PER_PAGE))
        if per_page not in PER_PAGE_OPTIONS:
            per_page = DEFAULT_PER_PAGE
    except (ValueError, TypeError):
        per_page = DEFAULT_PER_PAGE

    products = Product.objects.select_related("category").all()
    if category_slug:
        products = products.filter(category__slug=category_slug)

    paginator = Paginator(products, per_page)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "catalog/product_list.html", {
        "categories": categories,
        "products": page,
        "selected_category": category_slug,
        "per_page": per_page,
        "per_page_options": PER_PAGE_OPTIONS,
    })
