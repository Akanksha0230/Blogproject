from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment, Like, Tag, User
from .forms import BlogForm, CommentForm, RegisterForm, ProfileUpdateForm,CustomPasswordResetForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.utils import timezone


def base_generic(request):
    return render(request, 'base_generic.html')

def blog_list(request):
    blogs = Blog.objects.all().order_by('-date')
    search_query = request.GET.get('q', '')
    tag_filter = request.GET.get('tag', '')

    if search_query:
        blogs = blogs.filter(title__icontains=search_query)
    if tag_filter:
        blogs = blogs.filter(tags__name=tag_filter)

    return render(request, 'blog_list.html', {'blogs': blogs})

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
                    tag = Tag.objects.get_or_create(name=name)
                    tags.append(tag)
                except Exception as e:
                    print(f"Error creating or getting tag: {name} - {str(e)}")
                    return JsonResponse({'success': False, 'errors': {'tags': [f'Error creating or getting tag: {name}']}})
            print(tags)
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            blog.tags.set([tag.id for tag in tags])
            
            return JsonResponse({'success': True, 'redirect_url': '/bloglist/'})
        else:
            print(f"Form errors: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'errors': ['Invalid request method.']})


@login_required
def comment_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('blog_detail', blog_id=blog.id)
        else:
            messages.error(request, 'Error adding comment. Please correct the errors below.')
    else:
        form = CommentForm()
    return render(request, 'comment_blog.html', {'form': form})

@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    Like.objects.get_or_create(blog=blog, user=request.user)
    messages.success(request, 'Blog liked successfully.')
    return redirect('blog_detail', blog_id=blog.id)


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

User = get_user_model()


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        # Custom logic for sending reset email
        self.request.session['reset_email'] = form.cleaned_data['email']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_email'] = self.request.session.pop('reset_email', None)
        return context
    


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('blog_list')  # Redirect to your blog list page after profile update
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile_update.html', {'form': form})