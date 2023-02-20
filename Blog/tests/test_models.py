from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from Blog.models import Post, Category, Comment

class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin")
        


    # category model tests
    def create_category(self, name="Mental Health", slug="mental-health"):
        return Category.objects.create(name=name,slug=slug,publish=timezone.now())    

    def test_category_creation(self):
        category = self.create_category()
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), category.name)

    # post model tests
    def create_post(self, title="only a test",slug ="only-a-test",body="yes, this is only a test",category=""):
        return Post.objects.create(author=self.user,title=title, body=body,\
                                    publish=timezone.now(),photo=self.poster,\
                                    category=self.create_category(),
                                    status="published",featured=False)

    def test_post_creation(self):
        post = self.create_post()
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__str__(), post.title)


    # comment model tests
    def create_comment(self,name="Antonnifo", email="test@gmail.com",body= "well done"):
        return Comment.objects.create(post=self.create_post(category=self.create_category(name="Mental Health1", slug="mental-health1")), name=name,\
                                        email=email, body=body,publish=timezone.now(), \
                                        active=True)    

    # def test_comment_creation(self):
    #     comment = self.create_comment()
    #     self.assertTrue(isinstance(comment, Comment))
    #     self.assertEqual(comment.__str__(), 'Comment by Antonnifo on {}'.format(self.create_post()))


    # def test_whatever_list_view(self):
    #     w = self.create_whatever()
    #     url = reverse("whatever.views.whatever")
    #     resp = self.client.get(url)

    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn(w.title, resp.content)