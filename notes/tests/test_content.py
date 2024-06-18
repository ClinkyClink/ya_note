from django.contrib.auth import get_user_model

from notes.tests.common import CommonTest, URL
from notes.forms import NoteForm


User = get_user_model()


class TestContent(CommonTest):


    def test_list_of_notes_for_different_users(self):
        clients = (
            (self.author_client, True),
            (self.user_client, False),
        )
        for client, value in clients:
            with self.subTest(client=client):
                object_list = client.get(URL.list).context['object_list']
                if value:
                    self.assertIn(self.note, object_list)
                else:
                    self.assertNotIn(self.note, object_list)


    def test_authorized_client_has_form(self):
        for url in (URL.add, URL.edit):
            response = self.author_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.context['form'], NoteForm)