from django.contrib import admin

# Register your models here.
from app.models import ArticleCategory, Article

admin.site.register(ArticleCategory)
admin.site.register(Article)
