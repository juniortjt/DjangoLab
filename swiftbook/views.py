from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm, ContactForm, DocumentForm
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.template.loader import get_template
import datetime
from django.http import HttpResponse
from photologue.models import Photo
from django.views.generic import CreateView

class PhotoCreate(CreateView):
    model = Photo

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    now = datetime.datetime.now()

    # create a dict with the years and months:events
    post_dict = {}
    for i in range(posts[0].published_date.year, posts[len(posts) - 1].published_date.year - 1, -1):
        post_dict[i] = {}
        for month in range(1, 13):
            post_dict[i][month] = []
    for post in posts:
        post_dict[post.published_date.year][post.published_date.month].append(post)

    # this is necessary for the years to be sorted
    post_sorted_keys = list(reversed(sorted(post_dict.keys())))
    list_posts = []
    for key in post_sorted_keys:
        adict = {key: post_dict[key]}
        list_posts.append(adict)

    return render(request, 'swiftbook/post_list.html', {'posts': posts, 'now': now, 'list_posts': list_posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    now = datetime.datetime.now()

    # create a dict with the years and months:events
    post_dict = {}
    for i in range(posts[0].published_date.year, posts[len(posts) - 1].published_date.year - 1, -1):
        post_dict[i] = {}
        for month in range(1, 13):
            post_dict[i][month] = []
    for pst in posts:
        post_dict[pst.published_date.year][pst.published_date.month].append(pst)

    # this is necessary for the years to be sorted
    post_sorted_keys = list(reversed(sorted(post_dict.keys())))
    list_posts = []
    for key in post_sorted_keys:
        adict = {key: post_dict[key]}
        list_posts.append(adict)

    return render(request, 'swiftbook/post_detail.html', {'post': post,  'now': now, 'list_posts': list_posts})


def post_index(request):
    posts = Post.objects.filter().order_by('-published_date')
    now = datetime.datetime.now()

    # create a dict with the years and months:events
    post_dict = {}
    for i in range(posts[0].published_date.year, posts[len(posts) - 1].published_date.year - 1, -1):
        post_dict[i] = {}
        for month in range(1, 13):
            post_dict[i][month] = []
    for post in posts:
        post_dict[post.published_date.year][post.published_date.month].append(post)

    # this is necessary for the years to be sorted
    post_sorted_keys = list(reversed(sorted(post_dict.keys())))
    list_posts = []
    for key in post_sorted_keys:
        adict = {key: post_dict[key]}
        list_posts.append(adict)

    t = loader.get_template('swiftbook/temp.html')
    c = Context({
        'now': now, 'list_posts': list_posts,
    })
    return HttpResponse(t.render(c))


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'swiftbook/post_new.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'swiftbook/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'swiftbook/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

@login_required
def contact(request):
    form_class = ContactForm
    # new logic!

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', request.user)
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Swiftbook" +'',
                ['kacper267@op.pl'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')

    return render(request, 'contact.html', {'form': form_class,})


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = DocumentForm()
    return render(request, 'swiftbook/temp.html', {
        'form': form
    })

