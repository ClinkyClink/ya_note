from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model 

from notes.models import Note


client = Client()
User = get_user_model()
ANON = 'Аноним'
AUTHOR = 'Автор'
USER = 'Пользователь'
SLUG = 'detail_slug'
TITLE = 'Заголовок'
TEXT = 'Текст'


class URL_NAME:
    def __init__(self, home, add, list, detail, edit, delete, success, login, logout, signup):
        self.home = home
        self.add = add
        self.list = list
        self.detail = detail
        self.edit = edit
        self.delete = delete
        self.success = success
        self.login = login
        self.logout = logout
        self.signup = signup


URL = URL_NAME(
    reverse('notes:home'),
    reverse('notes:add'),
    reverse('notes:list'),
    reverse('notes:detail', args=(SLUG,)),
    reverse('notes:edit', args=(SLUG,)),
    reverse('notes:delete', args=(SLUG,)),
    reverse('notes:success'),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)

class CommonTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username=AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = User.objects.create(username=USER)
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.note = Note.objects.create(
            title=TITLE,
            text=TEXT,
            slug=SLUG,
            author=cls.author
        )