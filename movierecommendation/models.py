from django.db import models

# Create your models here.
class DoubanMovie(models.Model):
    movie_url = models.CharField(max_length=256)
    movie_title = models.CharField(max_length=64)
    movie_keywords = models.TextField()
    movie_description = models.TextField()
    movie_directors = models.TextField()
    movie_actors = models.TextField()
    def __str__(self):
        return self.movie_title

# 创建索引表
class DoubanMovieIndex(models.Model):
    movie_keyword = models.CharField(max_length=256)
    movie_doclist = models.TextField()
    def __str__(self):
        return self.movie_keyword



# 微博表
class WeiboComments(models.Model):
    comment_id = models.BigIntegerField(null=True)
    create_date_time = models.DateTimeField(null=True)
    content = models.TextField(null=True)
    sub_comment_count = models.IntegerField(null=True)
    comment_like_count = models.IntegerField(null=True)
    ip_location = models.CharField(max_length=255, null=True)
    user_id = models.BigIntegerField(null=True)
    nickname = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=1, null=True)

# 创建索引表
class WeiboCommentIndex(models.Model):
    comment_keyword = models.CharField(max_length=256)
    comment_doclist = models.TextField()
    def __str__(self):
        return self.comment_keyword

# 微博表
class WeiboNotes(models.Model):
    note_id = models.BigIntegerField(null=True)
    content = models.TextField(null=True)
    create_date_time = models.DateTimeField(null=True)
    liked_count = models.IntegerField(null=True)
    comments_count = models.IntegerField(null=True)
    shared_count = models.IntegerField(null=True)
    ip_location = models.CharField(max_length=255, null=True)
    user_id = models.BigIntegerField(null=True)
    nickname = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=1, null=True)

class WeiboNoteIndex(models.Model):
    note_keyword = models.CharField(max_length=256)
    note_doclist = models.TextField()

    def __str__(self):
        return self.note_keyword