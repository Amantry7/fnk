from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import ConsultRequestForm


def index(request):
    form = ConsultRequestForm()
    return render(request, 'main/index.html', {'form': form})


@require_POST
def submit_request(request):
    form = ConsultRequestForm(request.POST)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if form.is_valid():
        form.save()
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
