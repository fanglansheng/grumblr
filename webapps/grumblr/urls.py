"""webapps URL Configuration
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'grumblr.views.home', name='home-page'),

    url(r'^register$', 'grumblr.views.register', name='register-page'),

    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login',
        {'template_name':'grumblr/login.html'}, name='login-page'),
    # Route to logout a user and send them back to the login page

    url(r'^logout$', 'django.contrib.auth.views.logout_then_login',name='logout-page'),

    url(r'^add_post$','grumblr.views.addPost', name='add-new-post'),
    
    url(r'^go_following$','grumblr.views.following', name='following-page'),
    
    url(r'^go_profile/(?P<username>\w+)$', 'grumblr.views.goPofile', name='profile-page'),
    
    url(r'^go_stream$', 'grumblr.views.goStream', name='stream-page'),
    url(r'^follower_stream$', 'grumblr.views.followerStream', name='follower-stream-page'),

    url(r'^edit_profile$', 'grumblr.views.editProfile', name='edit-profile-page'),
    
    url(r'^get_profile_photo/(?P<username>\w+)$','grumblr.views.getProfilePhoto', name="profile-photo"),
    
    url(r'^forget_password$', 'grumblr.views.forgetPassword', name="forget-password"),
    
    url(r'^reset_password/(?P<username>.*)/(?P<token>.*)$', 'grumblr.views.resetPassword', name = "reset-password"),
    
    url(r'^emai_sent$', 'grumblr.views.emailSent', name="email-sent"),

    url(r'^follow/(?P<username>\w+)$', 'grumblr.views.follow', name="follow"),

    url(r'^unfollow/(?P<username>\w+)$', 'grumblr.views.unfollow', name="unfollow"),

    url(r'^stream/getPosts$', 'grumblr.views.getPosts'),
    
    url(r'^stream/getPosts/(?P<maxEntry>\d+)$', 'grumblr.views.getPosts', name="get-posts"),
    
    url(r'^stream/getChanges/(?P<maxEntry>\d+)$', 'grumblr.views.getChanges', name="stream-get-changes"),

    url(r'^add_comment/(?P<postId>\w+)$', 'grumblr.views.addComment', name = "add-comment"),

    url(r'^getCommentLists$', 'grumblr.views.getPostComments'),

    url(r'^getCommentChanges/(?P<commentMax>\d+)$', 'grumblr.views.getCommentChanges'),
]
