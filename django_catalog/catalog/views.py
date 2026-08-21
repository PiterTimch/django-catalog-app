from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

DEFAULT_PER_PAGE = 4
PER_PAGE_OPTIONS = [2, 4, 8, 12]


def get_custom_elided_page_range(paginator, number, on_each_side=1, on_ends=1):
    number = int(number)
    num_pages = paginator.num_pages

    if num_pages <= (on_each_side * 2 + on_ends * 2 + 1):
        return list(paginator.page_range)

    page_range = []

    # Left end
    for i in range(1, on_ends + 1):
        page_range.append(i)

    # Left ellipsis
    if number - on_each_side > on_ends + 1:
        page_range.append(paginator.ELLIPSIS)

    # Middle pages
    start = max(on_ends + 1, number - on_each_side)
    end = min(num_pages - on_ends, number + on_each_side)
    for i in range(start, end + 1):
        if i not in page_range:
            page_range.append(i)

    # Right ellipsis
    if number + on_each_side < num_pages - on_ends:
        page_range.append(paginator.ELLIPSIS)

    # Right end
    for i in range(num_pages - on_ends + 1, num_pages + 1):
        if i not in page_range:
            page_range.append(i)

    return page_range


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
    page_range = get_custom_elided_page_range(paginator, page.number, on_each_side=1, on_ends=1)

    return render(request, "catalog/product_list.html", {
        "categories": categories,
        "products": page,
        "page_range": page_range,
        "selected_category": category_slug,
        "per_page": per_page,
        "per_page_options": PER_PAGE_OPTIONS,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    return render(request, "catalog/product_detail.html", {"product": product})


def custom_page_not_found(request, exception):
    return render(request, "404.html", status=404)
