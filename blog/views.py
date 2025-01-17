from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment, Like, Tag, User
from .forms import BlogForm, RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.utils.timezone import localtime


def base_generic(request):
    return render(request, 'base_generic.html')


def blog_list(request):
    search_query = request.GET.get('q', '')
    tag_filter = request.GET.get('tag', '')

    blogs = Blog.objects.all().order_by('-date')

    if search_query:
        blogs = blogs.filter(title__icontains=search_query)
    if tag_filter:
        blogs = blogs.filter(tags__name=tag_filter)

    paginator = Paginator(blogs, 6)  # Show 6 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(request, 'blog_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'tag_filter': tag_filter,
        'tags': tags
    })

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.date = timezone.localtime(blog.date) 
    comments = blog.comments.all()
    return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments})


@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            

            # Process tags manually
            tags_input = request.POST.get('tags', '')
            print(f"Tags input: {tags_input}")
            tag_names = [name.strip() for name in tags_input.split(' ') if name.strip()]
            print(f"Processed tag names: {tag_names}")
            tags = []
            for name in tag_names:
                try:
                    tag, created  = Tag.objects.get_or_create(name=name)
                    tags.append(tag)
                except Exception as e:
                    print(f"Error creating or getting tag: {name} - {str(e)}")
                    return JsonResponse({'success': False, 'errors': {'tags': [f'Error creating or getting tag: {name}']}})
            print(f"Processed tag names: {tag_names}")
            print(f"Tags input: {tags_input}")
            print(f"Tags: {tags}")
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            blog.tags.set(tags)
            print(f"Blog created with ID: {blog.id} and Tags: {blog.tags.all()}") 
            
            return JsonResponse({'success': True, 'redirect_url': '/bloglist/'})
        else:
            print(f"Form errors: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'errors': ['Invalid request method.']})


@login_required
def update_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        blog = get_object_or_404(Blog, title=title)

        # Check if the logged-in user is the author of the blog
        if blog.author != request.user:
            return JsonResponse({'success': False, 'error': 'You are not authorized to update this blog.'})
        
        # Update the blog fields
        blog.content = request.POST.get('content')
        
        tags = request.POST.get('tags')
        if tags:
            tag_names = tags.split(' ')
            tag_ids = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                tag_ids.append(tag.id)
            blog.tags.set(tag_ids)
        
        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        
        blog.save()
        return JsonResponse({'success': True, 'redirect_url': '/bloglist/'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@login_required
def delete_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        blog = get_object_or_404(Blog, title=title)
        
        # Check if the logged-in user is the author of the blog
        if blog.author != request.user:
            return JsonResponse({'success': False, 'error': 'You are not authorized to delete this blog.'})
        
        blog.delete()
        return JsonResponse({'success': True, 'redirect_url': '/bloglist/'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': ['Error in authentication after registration.']})
        else:
            errors = [error for error in form.errors.values()]
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'errors': ['Invalid request method.']})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': ['Invalid username or password.']})
        else:
            errors = [error for error in form.errors.values()]
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'errors': ['Invalid request method.']})

def logout_view(request):
    print('Request method:', request.method)
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    print('Invalid request method:', request.method)
    return JsonResponse({'success': False, 'errors': ['Invalid request method.']})

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required'})
        otp = get_random_string(length=6, allowed_chars='0123456789')
        
        request.session['otp'] = otp
        request.session['email'] = email
        try:
          send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
          )
          print(f"Email sent to {email} with OTP {otp}")
          return JsonResponse({'success': True})
        except Exception as e:
            print(f"Failed to send email: {e}")
            return JsonResponse({'success': False, 'message': 'Failed to send email'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')
        
        if otp == request.session.get('otp') and email == request.session.get('email'):
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Invalid OTP'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'message': 'Passwords do not match'})

        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def like_blog(request, blog_id):
    if request.method == 'POST':
        try:
            blog = Blog.objects.get(id=blog_id)
            if request.user != blog.author:
                like, created = Like.objects.get_or_create(user=request.user, blog=blog)
                if created:
                    blog.likes = Like.objects.filter(blog=blog).count()
                    blog.save()
                    return JsonResponse({'success': True, 'likes': blog.likes})
                else:
                    return JsonResponse({'success': False, 'message': 'You have already liked this blog.'})
            else:
                return JsonResponse({'success': False, 'message': 'You cannot like your own blog.'})
        except Blog.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Blog not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



@login_required
def add_comment(request, blog_id):
    if request.method == 'POST':
      content = request.POST.get('content')
      if not content:
          return JsonResponse({'success': False, 'message': 'Comment content cannot be empty.'})

      blog = get_object_or_404(Blog, id=blog_id)
      comment = Comment.objects.create(blog=blog, user=request.user, content=content)

      return JsonResponse({
          'success': True,
          'comment': {
              'content': comment.content,
              'user': comment.user.username,
              'date': comment.date.strftime("%d %b %Y %H:%M")
          }
      })
    


def profile_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = request.user
        user_blogs = Blog.objects.filter(author=user)
        blog_titles = [{'id': blog.id,'title': blog.title, 'date': localtime(blog.date).strftime("%d %b %Y %I:%M %p")} for blog in user_blogs]
        return JsonResponse({'blog_titles': blog_titles})
    else:
        return render(request, 'base_generic.html') 
    




    