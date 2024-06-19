from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


client = Client()
User = get_user_model()
ANON = 'Аноним'
AUTHOR = 'Автор'
USER = 'Пользователь'
SLUG = 'detail_slug'
TITLE = 'Заголовок'
TEXT = 'Текст'


URL_NAME_IN_VIEWS = namedtuple(
    'NAME', (
        'home',
        'login',
        'logout',
        'signup',
        'add',
        'success',
        'list',
        'detail',
        'edit',
        'delete',
    )
)
URL = URL_NAME_IN_VIEWS(
    reverse('notes:home'),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
    reverse('notes:add'),
    reverse('notes:success'),
    reverse('notes:list'),
    reverse('notes:detail', args=(SLUG,)),
    reverse('notes:edit', args=(SLUG,)),
    reverse('notes:delete', args=(SLUG,)),
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
        cls.first_note = {
            'title': 'Заголовок',
            'text': 'Текст',
            'slug': 'slug_1',
            'author': cls.author,
        }
        cls.second_note = {
            'title': 'Заголовок',
            'text': 'Текст',
            'slug': 'slug_2',
        }
        cls.note_add = cls.author_client.post(
            reverse('notes:add'), data=cls.first_note
        )
        cls.edit_note_url = reverse(
            'notes:edit', args=(cls.first_note['slug'],)
        )
        cls.start_notes_count = Note.objects.count()
