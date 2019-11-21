from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import EmailMultiAlternatives
import os


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


def url_for_create_project(request, project_id):
    host = 'http://' + request.get_host()
    dest_path = '/acompanhamento-diario/projeto/'
    full_url = host + dest_path + str(project_id)

    return full_url


def send_email(subject_email, content_html):
    email_to = os.environ.get('EMAIL_TO')
    if email_to:
        subject, from_email, to = subject_email, 'from@example.com', email_to
        text_content = 'This is an important message.'
        html_content = content_html
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
