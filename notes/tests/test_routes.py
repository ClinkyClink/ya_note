from http import HTTPStatus

from notes.tests.common import CommonTest, URL


class TestRoutes(CommonTest):


    def test_pages_availability_for_different_users(self):
        urls = (
            (URL.home, self.client, HTTPStatus.OK),
            (URL.login, self.client, HTTPStatus.OK),
            (URL.logout, self.client, HTTPStatus.OK),
            (URL.signup, self.client, HTTPStatus.OK),
            (URL.detail, self.author_client, HTTPStatus.OK),
            (URL.edit, self.author_client, HTTPStatus.OK),
            (URL.delete, self.author_client, HTTPStatus.OK),
            (URL.add, self.user_client, HTTPStatus.OK),
            (URL.list, self.user_client, HTTPStatus.OK),
            (URL.success, self.user_client, HTTPStatus.OK),
            (URL.detail, self.user_client, HTTPStatus.NOT_FOUND),
            (URL.edit, self.user_client, HTTPStatus.NOT_FOUND),
            (URL.delete, self.user_client, HTTPStatus.NOT_FOUND),
            (URL.detail, self.client, HTTPStatus.FOUND), 
            (URL.edit, self.client, HTTPStatus.FOUND), 
            (URL.delete, self.client, HTTPStatus.FOUND), 

        )
        for url, client, expected_status in urls:
            with self.subTest(url=url):
                self.assertEqual(client.get(url).status_code, expected_status)


    def test_redirects(self):
        urls = (
            URL.list,
            URL.add,
            URL.success,
            URL.detail,
            URL.edit,
            URL.delete,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{URL.login}?next={url}'
                self.assertRedirects(self.client.get(url), redirect_url)