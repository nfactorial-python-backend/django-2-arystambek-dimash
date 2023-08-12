from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.core.paginator import Paginator
from .models import News, Comment


def home(request):
    return render(request, 'news/home.html')


def news(request):
    news_list = News.objects.order_by("-created_at")
    paginator = Paginator(news_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'news/news.html', context)


def detail(request, news_id):
    news_obj = get_object_or_404(News, pk=news_id)
    news_instance = News.objects.get(pk=news_id)
    comments = Comment.objects.order_by('-created_at').filter(news=news_instance)
    context = {"news_obj": news_obj, "comments": comments}
    return render(request, 'news/detail.html', context)


def comment(request, news_id):
    comment_post = request.POST["comment"]
    if comment_post != "":
        news_instance = News.objects.get(pk=news_id)
        comment_save_db = Comment(content=comment_post, news=news_instance)
        comment_save_db.save()

        return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))
    return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))


def news_post(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        content = request.POST["content"]
        if title and content:
            news_obj = News(title=title, description=description, content=content)
            news_obj.save()
            return HttpResponseRedirect(reverse("news:detail", args=(news_obj.id,)))
    return render(request, "news/post.html")
