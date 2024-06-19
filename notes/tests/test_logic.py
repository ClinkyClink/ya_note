from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note

from pytils.translit import slugify

from .common import CommonTest


User = get_user_model()


class TestLogic(CommonTest):

    def add_post(self, note_data):
        return self.author_client.post(
            reverse('notes:add'), data=note_data
        )

    def assert_note(self, note_data):
        note = Note.objects.get(slug=note_data['slug'])
        self.assertEqual(note.title, note_data['title'])
        self.assertEqual(note.text, note_data['text'])
        self.assertEqual(note.slug, note_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_user_can_create_note(self):
        self.assertRedirects(
            self.add_post(self.second_note), reverse('notes:success')
        )
        self.assertEqual(Note.objects.count(), self.start_notes_count + 1)
        self.assert_note(self.second_note)

    def test_anonymous_user_cant_create_note(self):
        url = reverse('notes:add')
        response = self.client.post(url, data=self.second_note)
        login_url = reverse('users:login')
        self.assertRedirects(response, f'{login_url}?next={url}')
        self.assertEqual(Note.objects.count(), self.start_notes_count)

    def test_not_unique_slug(self):
        add_post = self.add_post(self.first_note)
        slug = Note.objects.last().slug
        self.assertFormError(
            add_post, 'form', 'slug', errors=(slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), self.start_notes_count)

    def test_empty_slug(self):
        self.second_note.pop('slug')
        self.assertRedirects(self.add_post(self.second_note),
                             reverse('notes:success'))
        self.assertEqual(Note.objects.count(), self.start_notes_count + 1)
        new_note = Note.objects.last()
        expected_slug = slugify(self.second_note['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.edit_note_url,
                                           self.second_note)
        self.assertRedirects(response, reverse('notes:success'))
        self.assert_note(self.second_note)

    def test_other_user_cant_edit_note(self):
        response = self.user_client.post(self.edit_note_url, self.first_note)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assert_note(self.first_note)

    def test_author_can_delete_note(self):
        response = self.author_client.delete(
            reverse('notes:delete', args=(self.first_note['slug'],))
        )
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), self.start_notes_count - 1)

    def test_other_user_cant_delete_note(self):
        url = reverse('notes:delete', args=(Note.objects.last().slug,))
        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), self.start_notes_count)
