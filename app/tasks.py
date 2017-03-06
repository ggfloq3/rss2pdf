import requests
from django.core.mail import EmailMessage
from app.models import Article
from django.template import Context
from django.template.loader import get_template

from app.parser import Parser
from rss2pdf.celery import app
import pdfkit


@app.task()
def get_articles(url='https://lenta.ru/rss/news'):
    p = Parser(url)
    p.create_articles()


@app.task()
def process_pdf(email, categories, date1, date2):
    articles = Article.objects.filter(date__range=(date1, date2), category_id__in=categories).order_by('date')
    data = {
        'articles': articles
    }
    template = get_template('app/digest.html')
    html = template.render(Context(data))
    with open('out.pdf', "w+b") as file:
        pdfkit.from_string(html, 'out.pdf')
        email = EmailMessage(
            'Ваш дайджест новостей',
            'Во вложении',
            'ggfloq3@gmail.com',
            [email, ],
            headers={'Message-ID': 'foo'},
        )
        email.attach('articles.pdf', file.read(), 'application/pdf')
        email.send()

# def send_message(email, file):
#     return requests.post(
#         "https://api.mailgun.net/v3/sandbox153aa2f769c542bca86dde2afe62988f.mailgun.org/messages",
#         auth=("api", "key-89e515ac312783721a3e43f5da0db03d"),
#         files=[("attachment", file)],
#         data={"from": "Mailgun Sandbox <postmaster@sandbox153aa2f769c542bca86dde2afe62988f.mailgun.org>",
#               "to": "anton <ggfloq3@gmail.com>",
#               "subject": "Ваш дайджест новостей",
#               "text": "Вложение."})
