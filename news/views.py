from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.paginator import Paginator
from .models import News, Comment
from .forms import NewsForm, SignUpForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .serializers import NewsSerializer
from rest_framework import generics,status,serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
        comment_save_db = Comment(content=comment_post, news=news_instance, author=request.user)
        comment_save_db.save()

        return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))
    return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))


@login_required(login_url="/login")
@permission_required("news.add_news", login_url="/login")
def news_post(request):
    if request.method == "POST":
        form_post = NewsForm(request.POST)
        if form_post.is_valid():
            post = form_post.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse("news:detail", args=(post.id,)))
    else:
        form_post = NewsForm(request.POST)
    return render(request, "news/post.html", {"form_post": form_post})


class NewsUpdate(View):
    @method_decorator(login_required(login_url="/login/"))
    def get(self, request, news_id):
        news_obj = get_object_or_404(News, pk=news_id)
        form_change = NewsForm(instance=news_obj)
        return render(request, "news/change.html", {"form_change": form_change, "news_data": news_obj})

    @method_decorator(login_required(login_url="/login/"))
    @method_decorator(permission_required("news.add_news", login_url="/login/"))
    def post(self, request, news_id):
        news_obj = get_object_or_404(News, pk=news_id)
        form_change = NewsForm(request.POST, instance=news_obj)
        if request.user == news_obj.author:
            if form_change.is_valid():
                update = form_change.save()
                messages.success(request, "You successfully updated the post")
                return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))
        return render(request, "news/change.html", {"form_change": form_change, "news_data": news_obj})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="default")
            group.user_set.add(user)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {"form": form})


@permission_required("news.delete_news", login_url="/login")
def delete_news(request, news_id):
    news_db = get_object_or_404(News, pk=news_id)
    if request.method == "POST":
        if news_db.author == request.user or request.user.has_perm("comment.delete_comment"):
            news_db.delete()

    return redirect(reverse("news:news"))


@permission_required("comment.delete_comment", login_url="/login")
def delete_comment(request, news_id, comment_id):
    news_db = get_object_or_404(News, pk=news_id)
    comment_db = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        if request.user.username == comment_db.author.username or request.user.has_perm("comment.delete_comment"):
            comment_db.delete()

    return redirect(reverse("news:detail", args=(news_db.id,)))


@api_view(["POST", "GET"])
def news_api(request):
    if request.method == "POST":
        news_serializer = NewsSerializer(data=request.data)
        news_serializer["author"] = request.user
        if news_serializer.is_valid():
            news_serializer.save()
            return Response(news_serializer.data,status=status.HTTP_201_CREATED)

        return Response(news_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        news_queryset = News.objects.all()
        serializer = NewsSerializer(news_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewsDetail(generics.RetrieveDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer



