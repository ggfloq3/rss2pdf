from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
from app.models import ArticleCategory, Article


class Parser:
    """
        Получение записей в _parse_items
        Создание - create_articles
    """
    def __init__(self, url):
        self.url = url
        # словарь категорий вида { название:id } для быстрого получения id категории по её имени.
        # см. _cat_id_from_name
        self._categories_dict = {cat_title: cat_id for cat_id, cat_title
                                 in ArticleCategory.objects.values_list('id', 'title')}

    def _get_soup(self):
        with urllib.request.urlopen(self.url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'xml')
        return soup

    def _parse_items(self):
        soup = self._get_soup()
        items = soup.find_all('item')
        parsed_items = [
            {'title': x.title.string,
             'guid': x.guid.string,
             'description': x.description.string.strip(),
             'category_id': self._cat_id_from_name(x.category.string),
             'date': self._strip_time(x.pubDate.string), }
            for x in items]
        return parsed_items

    def create_articles(self):
        # Перед созданием отсеиваются уже существующие в базе записи.
        items = self._parse_items()
        guids = (x['guid'] for x in items)
        already_existing_guids = set(
            Article.objects.filter(guid__in=guids).values_list('guid', flat=True))
        filtered_items = filter(lambda x: x['guid'] not in already_existing_guids, items)
        articles = [Article(**item) for item in filtered_items]
        print('articles to create :', len(articles))
        Article.objects.bulk_create(articles)
        return len(articles)

    @staticmethod
    def _strip_time(string):
        dt = datetime.strptime(string, "%a, %d %b %Y %H:%M:%S %z")
        return dt

    def _cat_id_from_name(self, name):
        try:
            category_id = self._categories_dict[name]
        except KeyError:
            print('category created', name)
            new_category = ArticleCategory(title=name)
            new_category.save()
            self._categories_dict[name] = new_category.id
            category_id = new_category.id
        return category_id
