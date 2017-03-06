import json
import datetime
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView
from django.views.generic import TemplateView

from app.forms import MyForm
from app.models import ArticleCategory, Article
from app.tasks import process_pdf


class GetJsonData(View):
    """
        данные для формы - список категорий и границы доступных дат
    """

    def get(self, request):
        date_min = Article.objects.earliest('date').date
        date_max = Article.objects.latest('date').date
        data = {
            'categories': list(ArticleCategory.objects.values('id', 'title')),
            'date_min': date_min.strftime('%Y-%m-%d'),
            'date_max': date_max.strftime('%Y-%m-%d')
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


class MyFormView(FormView):
    form_class = MyForm
    template_name = 'app/form1.html'

    def get_form(self, form_class=None):
        form = super(MyFormView, self).get_form(form_class)
        data = self.request.body.decode('utf-8')
        if data:
            form.data = json.loads(data)
        return form

    def form_invalid(self, form):
        errors = [x[0] for x in form.errors.values()]
        return HttpResponse(json.dumps({'errors': errors}), content_type='application/json')

    def form_valid(self, form):
        """
        При успешной валидации формы выполняется process_PDF - там генерация файла и отправка письма
        """
        email = form.cleaned_data['email']
        categories = form.data['categories']
        date1 = form.cleaned_data['date1']
        date2 = form.cleaned_data['date2']
        process_pdf.delay(email, categories, date1, date2)
        articles_count = Article.objects.filter(date__range=(date1, date2), category_id__in=categories).count()
        return HttpResponse(json.dumps({
            'success': True,
            'message': '{} articles'.format(articles_count)
        }), content_type='application/json')


class DemoDigest(TemplateView):
    template_name = 'app/digest.html'

    def get_context_data(self, **kwargs):
        context = super(DemoDigest, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.order_by('date')[:100]
        return context
