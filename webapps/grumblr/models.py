from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

class Profile(models.Model):
    owner = models.OneToOneField(User, primary_key=True,related_name="profile")
    age = models.IntegerField(default = 0, null=True, blank=True)
    city = models.CharField(max_length = 20, blank = True)
    country = models.CharField(max_length = 20, blank = True)
    bio = models.CharField(max_length = 420, blank = True)
    picture = models.ImageField(upload_to="profile_pictures", default='profile_pictures/default_photo.jpg', blank = True)
    following = models.ManyToManyField(User, related_name = "following", blank=True, null=True)
    
    def __unicode__(self):
        return self.owner.username

class Posts(models.Model):
    owner = models.ForeignKey(User)
    text = models.CharField(max_length=42)
    date = models.DateTimeField(auto_now = True)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.text

    # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(logentry_id=-1):
        return Posts.objects.filter(postlog__gt=logentry_id).distinct()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_items(logentry_id=-1):
        return Posts.objects.filter(deleted=False,
                        postlog__gt=logentry_id).order_by('-date').distinct()

class PostLog(models.Model):
    item = models.ForeignKey(Posts)
    op   = models.CharField(max_length=3, choices=[('Add', 'add'),
                                                   ('Del', 'del')])
    def __unicode__(self):
        return "LogEntry (%d, %s, %s)" % (self.id, self.item, self.op)
    def __str__(self):
        return self.__unicode__()

    # Gets the id of the most recent LogEntry
    @staticmethod
    def get_max_id():
        return PostLog.objects.all().aggregate(Max('id'))['id__max'] or 0

class Comments(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Posts)
    content = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now = True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.content)

    @staticmethod
    def get_changes(logentry_id=-1):
        return Comments.objects.filter(commentlog__gt=logentry_id).distinct()

class CommentLog(models.Model):
    item = models.ForeignKey(Comments)
    op   = models.CharField(max_length=3, choices=[('Add', 'add'),
                                                   ('Del', 'del')])
    def __unicode__(self):
        return "CommentLog (%d, %s, %s)" % (self.id, self.item, self.op)
    def __str__(self):
        return self.__unicode__()

    # Gets the id of the most recent LogEntry
    @staticmethod
    def get_max_id():
        return CommentLog.objects.all().aggregate(Max('id'))['id__max'] or 0

