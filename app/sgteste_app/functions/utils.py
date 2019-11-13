from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
def paginattion_create(obj_list, num_pages, request):
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_list, num_pages)
    try:
        obj_page = paginator.page(page)
        return obj_page
    except PageNotAnInteger:
        obj_page = paginator.page(1)
        return obj_page
    except EmptyPage:
        obj_page = paginator.page(paginator.num_pages)
        return obj_page