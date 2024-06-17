from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Не автор')
        cls.user_client = Client()
        cls.user_client.force_login(cls.author)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='slug',
            author=cls.author
        )

    def test_notes_count(self):
        response = self.user_client.get(reverse('notes:list'))
        notes_count = response.context['object_list'].count()
        self.assertEqual(notes_count, 1)

    def test_note_not_in_list_for_another_user(self):
        self.user_client.force_login(self.reader)
        response = self.user_client.get(reverse('notes:list'))
        notes_count = response.context['object_list'].count()
        self.assertEqual(notes_count, 0)

    def test_authorized_client_has_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for url, args in urls:
            with self.subTest(url=url):
                response = self.user_client.get(reverse(url, args=args))
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)