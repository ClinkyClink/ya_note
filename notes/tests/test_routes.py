from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()

class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='slug',
            author=cls.author
        )
        cls.urls_with_args = (
            ('notes:detail', (cls.note.slug,)),
            ('notes:edit', (cls.note.slug,)),
            ('notes:delete', (cls.note.slug,))
        )
        cls.urls = (
            ('notes:list', None),
            ('notes:add', None),
            ('notes:success', None),
        )

    def test_pages_availability_for_anonymous(self):
        urls = (
            'notes:home',
            'users:signup',
            'users:login',
            'users:logout',
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(reverse(url))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_note_availability_for_author(self):
        for name, args in self.urls:
            with self.subTest(name=name):
                self.client.force_login(self.author)
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_note_availability_for_reader(self):
        for name, args in self.urls_with_args:
            with self.subTest(name=name):
                self.client.force_login(self.reader)
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirect_for_anonymous(self):
        login_url = reverse('users:login')
        for name, args in self.urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)