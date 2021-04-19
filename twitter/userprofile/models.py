from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
import os
from django.conf import settings
import filetype
import ffmpeg
import ffmpeg_streaming
from ffmpeg_streaming import Formats
from threading import Thread


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    image = models.ImageField(verbose_name=_('profile image'), upload_to='user-profile-photos/', blank=True, null=True)
    biography = models.TextField(verbose_name=_('biography'), blank=True)


def convert_video_to_hls(arg, path_root):
    if not os.path.exists(path_root):
        os.makedirs(path_root)
    video = ffmpeg_streaming.input(str(settings.MEDIA_ROOT + arg.file.name))
    save_to = str(path_root + '/key')
    # A URL (or a path) to access the key on your website
    url = settings.MEDIA_URL + str(arg.id) + '/key'
    # or url = '/"PATH TO THE KEY DIRECTORY"/key';

    hls = video.hls(Formats.h264())
    hls.encryption(save_to, url)
    hls.auto_generate_representations()
    hls.output(str(path_root + '/hls.m3u8'))


class Tweet(models.Model):
    # foreign key to User this Tweet refers to
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('tweet owner'),
                               related_name='owner',blank=True, null=True)
    # TODO: Use a validator for minlength in the forms (too)!
    text = models.CharField(max_length=250, verbose_name=_('tweet body text'), validators=[MinLengthValidator(1)], 
        blank=True)
    file = models.FileField(verbose_name=_('tweet body file'), upload_to='userprofile/files', blank=True)
    create_datetime = models.DateTimeField(verbose_name=_("create date and time"), auto_now=False,
                                         auto_now_add=True)
    update_datetime = models.DateTimeField(verbose_name=_("update date and time"), auto_now=True,
                                         auto_now_add=False)
    retweet = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    like_count = models.IntegerField(default=0, null=True, blank=True)

    @property
    def filetype(self):
        kind = filetype.guess(self.file)
        if kind:
            if 'video' in kind.mime:
                return 'video'
            elif 'image' in kind.mime:
                return 'image'
        return ''

    # Override clean method to declare only one of text or image/videos are required
    # and not both of them can be blank at the same time
    def clean(self):
        """
        Require at least one of text or image/video to be set
        """
        # import pdb; pdb.set_trace()
        # This will check for None or Empty
        if not self.text and (not self.file or not self.file.name):
            raise ValidationError(_('Tweet body can\'t be empty, Even one of text or image/video should have a value.'))

    
    def save(self, *args, **kwargs):
        super(Tweet, self).save(*args, **kwargs)
        if self.text:
            # extract hashtags
            text = self.text
            tags = {tag.strip("#") for tag in text.split() if tag.startswith("#")}
            for tag in tags:
                queryset = HashTag.objects.filter(tag=tag)
                if len(queryset) == 0:
                    hashtag = HashTag.objects.create(tag=tag)
                else:
                    hashtag = queryset[0]
                    # check if this is the first time object is saved
                    tag_results = Tag.objects.filter(hashtag=hashtag, tweet=self)
                    if tag_results and len(tag_results) > 0:
                        continue
                Tag.objects.create(hashtag=hashtag, tweet=self)
        
        path_root = settings.MEDIA_ROOT + str(self.id)
        if self.filetype == 'video' and (not os.path.exists(path_root) or len(os.listdir(path_root)) == 0):
            # video Directory is empty
            thread = Thread(target = convert_video_to_hls, args = (self, path_root,))
            thread.start()

class Follow(models.Model):
    # foreign key to the user who is the follower 
    follower = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('follower'),
                               related_name='follower')
    # foreign key to the user who has been followed
    followed = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('followed'),
                               related_name='followed')
    follow_datetime = models.DateTimeField(verbose_name=_("follow date and time"), auto_now=False,
                                         auto_now_add=True)


class Like(models.Model):
    # foreign key to the user who has liked a tweet
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user liking a tweet'),
                               related_name='like_user')
    # foreign key to the tweet the user liked
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, verbose_name=_('tweet the user liked'),
                               related_name='like_tweet')
    like_datetime = models.DateTimeField(verbose_name=_("like date and time"), auto_now=False,
                                         auto_now_add=True)


# HashTag represents a table in databse having all
# unique tags used by all users
# The tweet and user id in which and by whom these tags are used
# is saved in Tag table
# This table is used for DRY and memory efficiency purposes
class HashTag(models.Model):
    # TODO: Use a validator for minlength in the forms (too)!
    tag = models.CharField(max_length=250, verbose_name=_('tag body'), validators=[MinLengthValidator(1)], 
        blank=True)


class Tag(models.Model):
    # foreign key to the hashtag used in this tag 
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE, verbose_name=_('referencing hashtag body'),
                               related_name='hashtag')
    # foreign key to the tweet in which this tag is used 
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, verbose_name=_('tweet containing this hashtag'),
                               related_name='tag_tweet')
    tag_datetime = models.DateTimeField(verbose_name=_("tag date and time"), auto_now=False,
                                         auto_now_add=True)