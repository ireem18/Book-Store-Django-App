from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginator(page, model):
    objects = model.objects.active()
    paginator = Paginator(objects, 3)

    try:
        page_objects = paginator.page(page)
    except PageNotAnInteger:
        page_objects = paginator.page(1)
    except EmptyPage:
        page_objects = paginator.page(paginator.num_pages)

    return page_objects