from datetime import timedelta

from django.test import TestCase
from .models import News, Comment
from django.urls import reverse
from django.utils import timezone


class NewsTest(TestCase):
    def test_has_comments_true(self):
        news = News(title="Tilte", content="Hello World")
        comment = Comment(content="Comment 1", news=news)
        news.save()
        comment.save()
        self.assertTrue(news.has_comments())

    def test_has_comment_false(self):
        news = News(title="This is News", content="Yeah this is new post")
        news.save()
        self.assertFalse(news.has_comments())


class NewsViewTest(TestCase):
    def test_view_news_page_order_by_desc_true(self):
        for count in range(1, 5):
            News(title=f"{count} - Title", content=f"{count} - Description",created_at=timezone.now() + timedelta(days=count)).save()
        response = self.client.get(reverse('news:news'))
        news_context = response.context['page_obj']
        sorted_news = News.objects.order_by('-created_at')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(news_context, sorted_news, ordered=True)

    def test_view_detail_exists(self):
        news = News.objects.create(title="Check Detail", content="It's Ok", created_at=timezone.now())
        response = self.client.get(reverse('news:detail', args=(news.id,)))
        detail_context = response.context["news_obj"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(detail_context.title, news.title)
        self.assertEqual(detail_context.content, news.content)

    def test_news_comments_ordered_by_desc_true(self):
        news = News.objects.create(title="Comment Title", content="This is post")

        comment = Comment.objects.create(news=news, content="Comment posted 1",created_at=timezone.now() + timedelta(days=1))
        comment2 = Comment.objects.create(news=news, content="Comment posted 2",created_at = timezone.now() + timedelta(days=2))
        response = self.client.get(reverse('news:detail', args=(news.id,)))
        comment_context = response.context["comments"]
        self.assertEqual(comment,comment_context[1])
        self.assertEqual(comment2,comment_context[0])

