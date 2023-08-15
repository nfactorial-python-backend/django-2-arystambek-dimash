from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.core.paginator import Paginator
from .models import News, Comment
from .forms import NewsForm
from django.views.generic.edit import UpdateView
from django.contrib import messages


def home(request):
    return render(request, 'news/home.html')


def news(request):
    news_list = News.objects.order_by("-created_at")
    paginator = Paginator(news_list, 10)

    page_number = request.GET.get(request, 'page')
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
        form_post = NewsForm(request.POST)
        if form_post.is_valid():
            post = form_post.save()
            post.save()
            return HttpResponseRedirect(reverse("news:detail", args=(post.id,)))
    else:
        form_post = NewsForm(request.POST)
    return render(request, "news/post.html", {"form_post": form_post})


class NewsUpdate(UpdateView):
    def get(self, request, news_id):
        news_obj = get_object_or_404(News, pk=news_id)
        form_change = NewsForm(request.POST, instance=news_obj)
        return render(request, "news/change.html", {"form_change": form_change, "news_data": news_obj})

    def post(self, request,news_id):
        news_obj = get_object_or_404(News, pk=news_id)
        form_change = NewsForm(request.POST, instance=news_obj)
        if form_change.is_valid():
            update = form_change.save(commit=False)
            update.save()
            messages.success(request, "You successfully updated the post")

            return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))
        return render(request, "news/change.html", {"form_change": form_change, "news_data": news_obj})

