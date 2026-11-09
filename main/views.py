from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .emails import send_request_notification
from .forms import ConsultRequestForm
from .models import News


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        f'Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml',
        '',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def index(request):
    form = ConsultRequestForm()
    return render(request, 'main/index.html', {'form': form})


def news_detail(request, slug):
    item = get_object_or_404(News, slug=slug, is_active=True)
    more = News.objects.filter(is_active=True).exclude(pk=item.pk)[:3]
    return render(request, 'main/news_detail.html', {'item': item, 'more': more})


@require_POST
def submit_request(request):
    form = ConsultRequestForm(request.POST)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if form.is_valid():
        req = form.save()
        send_request_notification(req)
        if is_ajax:
            return JsonResponse({
                'ok': True,
                'message': 'Спасибо! Заявка отправлена — мы свяжемся с вами в ближайшее время.',
            })
        messages.success(
            request,
            'Спасибо! Заявка отправлена — мы свяжемся с вами в ближайшее время.',
        )
        return redirect('index')

    if is_ajax:
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    messages.error(request, 'Проверьте правильность заполнения формы.')
    return render(request, 'main/index.html', {'form': form}, status=400)
