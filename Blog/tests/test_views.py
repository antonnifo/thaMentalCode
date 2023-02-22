from django.test import TestCase
from django.urls import reverse  
from django.utils import timezone
from Blog.models import Post, Category, Comment
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class HomepageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("blog:home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("blog:home"))
        self.assertTemplateUsed(response, "site/index.html")

    def test_template_content(self):
        response = self.client.get(reverse("blog:home"))
        self.assertContains(response, "<h2> No posts at the moment please check back later. </h2>")
        self.assertNotContains(response, "Not on the page")


class ListCategoryViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="admin")
        self.poster = SimpleUploadedFile(name='logo.png', content=open('Blog/static/images/logo/logo.png', 'rb').read())
        self.category = Category.objects.create(name="Mental Health",slug="mental-health",publish=timezone.now())
        self.post = Post.objects.create(author=self.user,title="only a test",slug ="only-a-test",body="yes, this is only a test",\
                                    publish=timezone.now(),photo=self.poster,\
                                    category=self.category,
                                    status="published",featured=False)  
        self.post.tags.add('tagz','tag1')  
        self.posts_by_category = self.category.posts.all()                              
     

    def test_GET_list_posts_by_category(self):
        # test url available by name
        response = self.client.get(reverse("blog:post_list_by_category", args=['mental-health']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Mental Health</title>", html=True)
        self.assertTemplateUsed(response, "site/category.html")

    def test_GET_list_posts_by_tag(self):
    
        response = self.client.get(reverse("blog:post_list_by_tag", args=['tagz']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>tagz</title>", html=True)
        self.assertTemplateUsed(response, "site/category.html")


    # def test_page_out_of_range(self):
    #     response = self.client.get(reverse("blog:post_list_by_category", args=['mental-health']))
    #     self.assertEquals(response.context['posts'].number, 2)


class PostDetailViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="admin")
        self.poster = SimpleUploadedFile(name='logo.png', content=open('Blog/static/images/logo/logo.png', 'rb').read())
        self.category = Category.objects.create(name="Mental Health",slug="mental-health",publish=timezone.now())
        self.post = Post.objects.create(author=self.user,title="only a test",slug ="only-a-test",body="yes, this is only a test",\
                                    publish=timezone.now(),photo=self.poster,\
                                    category=self.category,
                                    status="published",featured=False)  
        self.post.tags.add('tagz','tag1')

    def test_GET_post(self):
        response = self.client.get(reverse("blog:post_detail", args=[self.post.publish.year,\
                                            self.post.publish.month,
                                            self.post.publish.day,
                                            self.post.slug]))
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "<title>only a test</title>", html=True)
        self.assertTemplateUsed(response, "site/blog-detail.html") 

    def test_POST_comment(self):

        data = {"name": "Dombey Son",
               "email": "mail@example.com",
               "message": "another commen test",
               }
                                          
        response = self.client.post(reverse("blog:post_detail", args=[self.post.publish.year,\
                                            self.post.publish.month,
                                            self.post.publish.day,
                                            self.post.slug]), data=data)

        self.assertEqual(response.status_code, 200)
