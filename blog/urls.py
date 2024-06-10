from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.blog_list, name='blog_list'),
    path('', views.base_generic, name='base_generic'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/create/', views.create_blog, name='create_blog'),
    path('blog/update/', views.update_blog, name='update_blog'),
    path('blog/delete/', views.delete_blog, name='delete_blog'),
    path('like/<int:blog_id>/', views.like_blog, name='like_blog'),
    path('blog/<int:blog_id>/comment/', views.add_comment, name='add_comment'), 
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)