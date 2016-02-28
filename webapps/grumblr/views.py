from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.conf import settings

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core import serializers

from grumblr.models import *
from grumblr.forms import *

import json

@login_required
def home(request):
    context = {}
    context['user_full_name'] = request.user.get_full_name()
    context['profile'] = User.objects.get(username=request.user).profile
    if request.method == 'GET':
        context['postForm'] = PostForm()
    return render(request, 'grumblr/stream.html', context)

def register(request):

    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context = {'registerForm': RegisterForm()}
        return render(request, 'grumblr/signup.html', context)

    registerForm = RegisterForm(request.POST)
    context = {'registerForm': registerForm}

    if not registerForm.is_valid():
        return render(request, 'grumblr/signup.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=registerForm.cleaned_data['username'],
                                        first_name=registerForm.cleaned_data['first_name'],\
                                        last_name=registerForm.cleaned_data['last_name'],
                                        password=registerForm.cleaned_data['password1'],
                                        email = registerForm.cleaned_data['email'])

    # create empty profile for this user
    new_profile = Profile(owner=new_user)
    profile_form = EditProfileForm(request.POST, instance=new_profile)
    if not profile_form.is_valid():
        print profile_form.errors, "fail!!!!!!!!!"
        return render(request, 'grumblr/signup.html', context)
    profile_form.save()
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=registerForm.cleaned_data['username'],
                            password=registerForm.cleaned_data['password1'])
    login(request, new_user)
    return redirect('/')

@login_required
# @transaction.atomic
def addPost(request):
    new_post = Posts(owner=request.user)
    postForm = PostForm(request.POST, instance=new_post)

    if not postForm.is_valid():
        dic = {}
        error_str = postForm.errors.as_json()
        error_dict = json.loads(error_str)
        dic['type'] = 'error'
        dic['content'] = error_dict
        data = json.dumps(dic)
        return HttpResponse(data, content_type='application/json')
    # if not 'postContent' in request.POST or not request.POST['postContent']:
    #     raise Http404
    else:
        new_post.full_clean()
        new_post.save()
        postLog = PostLog(item=new_post, op='Add')
        postLog.save()

    print "save...."
    return HttpResponse("")
    # return redirect('home-page')

@login_required
def goPofile(request, username):
    context = {}
    user = get_object_or_404(User, username = username)
    context['user'] = user
    posts = Posts.objects.filter(owner = user).order_by('-date')
    context['posts'] = posts
    posts_count = posts.count()
    context['posts_count'] = posts_count
    currentUser = User.objects.get(username = request.user)
    context['currentUser'] = currentUser
    if currentUser.profile.following.filter(username = user):
        context['isfollowed'] = True
    else:
        context['isfollowed'] = False
    return render(request, 'grumblr/profile.html', context)

def goStream(request):
    return render(request, 'grumblr/login.html')

@login_required
def editProfile(request):
    context = {}
    context['user'] = request.user

    if request.method == 'GET':
        context['profile']=EditProfileForm()
        return render(request, 'grumblr/edit_profile.html', context)

    user_profile = get_object_or_404(Profile, owner=request.user)
    profile_form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

    if not profile_form.is_valid():
        context['profile'] = profile_form
        context['info'] = "You have some invalid inputs."
        return render(request, 'grumblr/edit_profile.html', context)
    profile_form.save()
    context['info'] = "Changes Saved!"
    context['profile']=EditProfileForm()
    return render(request, 'grumblr/edit_profile.html', context)

@login_required
def getProfilePhoto(request, username):
    user = User.objects.get(username = username)
    profile = get_object_or_404(Profile, owner=user)

    if not profile.picture:
        print "Cannot find this picture"
        raise Http404
    content_type = guess_type(profile.picture.name)
    return HttpResponse(profile.picture, content_type=content_type)

def resetPassword(request, username, token):
    context = {}
    context['username'] = username
    context['token'] = token

    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, token):
        raise Http404

    if request.method == 'GET':
        context['resetPassword'] = SetPasswordForm()
        return render(request, 'grumblr/resetPassword.html', context)

    resetForm = SetPasswordForm(request.POST)
    if not resetForm.is_valid():
        context['resetPassword'] = resetForm
        return render(request, 'grumblr/resetPassword.html', context)

    user = get_object_or_404(User, username = resetForm.cleaned_data['username'])
    new_password = resetForm.cleaned_data['password1']
    user.set_password(new_password)
    user.save()
    context['info'] = "save succeed."
    return render(request, 'grumblr/resetPassword.html', context)


def forgetPassword(request):
    context = {}
    context['isSent'] = False
    if request.method == "GET":
        context['emailForm'] = ForgetPasswordForm()
        return render(request, 'grumblr/forget_password.html', context)
    emailForm = ForgetPasswordForm(request.POST)

    if not emailForm.is_valid():
        context['emailForm'] = emailForm
        return render(request, 'grumblr/forget_password.html', context)

    user = User.objects.get(email = emailForm.cleaned_data['email'])
    sendEmail(request, user)
    context['info'] = "Reset password link has sent to you."
    context['isSent'] = True
    return render(request, 'grumblr/forget_password.html', context)

def emailSent(request):
    context = {}
    user = User.objects.get(username = request.user)
    if not user:
        context['info'] = "We dont have this user."
        return render(request, 'grumblr/email_sent.html',context)
    sendEmail(request, user)
    context['info'] = "Reset password email has sent to your registed email."
    return render(request, 'grumblr/email_sent.html',context)

def sendEmail(request, user):
    token = default_token_generator.make_token(user)

    message_body = """Welcome to Grumblr. Use the link below to reset your password.

    http://%s%s""" % (request.get_host(), reverse('reset-password', args=(user, token)))

    # user = User.objects.get(username = username)
    send_mail(subject = 'Reset Password | Grumblr',
        message= message_body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False)


@login_required
def followerStream(request):
    context = {}
    followers = request.user.profile.following.all()

    # filter_qs = Q()
    # for fw in followers:
    #     filter_qs = filter_qs | Q(owner__profile__following=fw)
    # my_model.objects.filter(filter_qs)

    posts = Posts.objects.filter(owner__profile__following=followers).order_by('-date').distinct()

    context['posts'] = posts
    return render(request, 'grumblr/followingStream.html', context)

@login_required
def following(request):
    context = {}
    user = get_object_or_404(User, username = request.user)
    following = user.profile.following.all()
    context['followingList'] = following
    
    return render(request, 'grumblr/following.html', context)

@login_required
def unfollow(request, username):
    user = User.objects.get(username = request.user)
    follow = get_object_or_404(User, username = username)
    user.profile.following.remove(follow)
    user.save()
    return redirect('profile-page', username = username)

@login_required
def follow(request, username):
    user = User.objects.get(username = request.user)
    follow = get_object_or_404(User, username = username)
    user.profile.following.add(follow)
    user.save()
    return redirect('profile-page', username = username)

def getPosts(request, maxEntry = -1):
    maxCount = PostLog.get_max_id()
    posts = Posts.get_items(maxEntry)
    content = {"maxCount":maxCount, "posts": posts}
    return render(request, 'grumblr/posts.json', content, content_type="application/json")

def getChanges(request, maxEntry=-1):
    maxCount = PostLog.get_max_id();
    posts = Posts.get_changes(maxEntry)
    content = {"maxCount" : maxCount, "posts": posts}
    return render(request, 'grumblr/posts.json', content, content_type="application/json")

# add comment to username
def addComment(request, postId):
    cur_post = Posts.objects.get(pk=postId)
    new_comment = Comments(user=request.user, post=cur_post)
    # fill comment form
    commentForm = CommentForm(request.POST, instance=new_comment)
    # validate form
    if not commentForm.is_valid():
        return HttpResponse("")
    # save comment
    commentForm.save()
    commentLog = CommentLog(item=new_comment, op='Add')
    commentLog.save()
    return HttpResponse("")

def getPostComments(request):
    maxCount = CommentLog.get_max_id()
    # get all posts in stream page
    posts = Posts.objects.all()
    # get commentList of each post
    commentLists = []
    for post in posts:
        commentList = Comments.objects.filter(post=post)
        if commentList:
            item = {}
            item["list"] = commentList
            item["postId"] = post.pk
            commentLists.append(item)
    content = {"maxCount":maxCount, "commentLists": commentLists}
    return render(request, 'grumblr/commentList.json', content, content_type="application/json")


def getComments(request, postId):
    cur_post = Posts.objects.get(pk=postId)
    comments = Comments.objects.filter(post=cur_post)
    content = {}
    return render(request, 'grumblr/commentList.json', content, content_type="application/json")

def getCommentChanges(request, commentMax=-1):
    maxCount = CommentLog.get_max_id();
    comments = Comments.get_changes(commentMax)
    # content = {"maxCount" : maxCount, "posts": posts}
    # get postIds
    postIdList = []
    for comment in comments:
        postId = comment.post.pk
        if postId not in postIdList:
            postIdList.append(comment.post.pk)

    # get commentList of each post
    commentLists = []
    for pId in postIdList:
        item = {}
        post = Posts.objects.get(pk=pId)
        # get all comments of selected post
        commentList = comments.filter(post = post)
        item["list"] = commentList
        item["postId"] = pId
        commentLists.append(item)

    content = {"maxCount":maxCount, "commentLists": commentLists}
    return render(request, 'grumblr/commentList.json', content, content_type="application/json")


