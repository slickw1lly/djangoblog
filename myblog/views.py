from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from myblog.models import Post, Category
from myblog.serializers import UserSerializer, GroupSerializer, PostSerializer, CatergorySerializer
from myblog.forms import PostForm


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'list.html', context)


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {'post': post}
    return render(request, 'detail.html', context)


def add_model(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.created_date = timezone.now()
            model_instance.modified_date = timezone.now()
            model_instance.published_date = timezone.now()
            model_instance.save()
            return redirect('/')
    else:
        form = PostForm()
        return render(request, "post_template.html", {'form': form})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CatergoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CatergorySerializer
