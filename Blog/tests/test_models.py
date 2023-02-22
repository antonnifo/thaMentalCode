from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from Blog.models import Post, Category, Comment

class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin")
        self.poster = SimpleUploadedFile(name='logo.png', content=open('Blog/static/images/logo/logo.png', 'rb').read())
        self.category = Category.objects.create(name="Mental Health",slug="mental-health",publish=timezone.now())
        self.post = Post.objects.create(author=self.user,title="only a test",slug ="only-a-test",body="yes, this is only a test",\
                                    publish=timezone.now(),photo=self.poster,\
                                    category=self.category,
                                    status="published",featured=False)  
        self.post.tags.add('tagz','tag1') 

        self.comment = Comment.objects.create(post=self.post, name="Antonnifo",\
                                        email='test@example.com', body='Another comment',publish=timezone.now(), \
                                        active=True)       

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(self.category.__str__(), self.category.name)

    def test_post_creation(self):
        post = self.post
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__str__(), post.title)

    def test_comment_creation(self):
        comment = self.comment
        self.assertTrue(isinstance(comment, Comment))
        self.assertEqual(comment.__str__(), 'Comment by Antonnifo on {}'.format(self.post))


