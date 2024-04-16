from django.contrib import admin
from import_export import resources
from movierecommendation.models import DoubanMovie, DoubanMovieIndex, WeiboComments, WeiboCommentIndex, WeiboNotes, \
    WeiboNoteIndex
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class MovieResource(resources.ModelResource):
    class Meta:
        model = DoubanMovie
        export_order = (
            'movie_url', 'movie_title', 'movie_keywords', 'movie_description', 'movie_directors', 'movie_actors')


@admin.register(DoubanMovie)
class MovieAdmin(ImportExportModelAdmin):
    list_display = (
        'movie_url', 'movie_title', 'movie_keywords', 'movie_description', 'movie_directors', 'movie_actors')
    search_fields = ('movie_title', 'movie_keywords', 'movie_description', 'movie_directors', 'movie_actors')
    resource_class = MovieResource


class MovieIndexResource(resources.ModelResource):
    class Meta:
        model = DoubanMovieIndex
        export_order = ('movie_keyword', 'movie_doclist')


@admin.register(DoubanMovieIndex)
class MovieIndexAdmin(ImportExportModelAdmin):
    list_display = ('movie_keyword', 'movie_doclist')
    search_field = ('movie_keyword')
    resource_class = MovieIndexResource


class WeiboCommentsResource(resources.ModelResource):
    class Meta:
        model = WeiboComments
        export_order = (
            'comment_id', 'create_date_time', 'content', 'sub_comment_count', 'comment_like_count', 'ip_location',
            'user_id', 'nickname', 'gender')


@admin.register(WeiboComments)
class WeiboCommentsAdmin(ImportExportModelAdmin):
    list_display = (
        'comment_id', 'create_date_time', 'content', 'sub_comment_count', 'comment_like_count', 'ip_location',
        'user_id',
        'nickname', 'gender')
    search_fields = ('content', 'nickname')
    resource_class = WeiboCommentsResource


class WeiboCommentIndexResource(resources.ModelResource):
    class Meta:
        model = WeiboCommentIndex
        export_order = ('comment_keyword', 'comment_doclist')

@admin.register(WeiboCommentIndex)
class WeiboCommentIndexAdmin(ImportExportModelAdmin):
    list_display = ('comment_keyword', 'comment_doclist')
    search_fields = ('comment_keyword',)
    resource_class = WeiboCommentIndexResource


class WeiboNotesResource(resources.ModelResource):
    class Meta:
        model = WeiboNotes
        export_order = ('note_id', 'content', 'create_date_time', 'liked_count', 'comments_count', 'shared_count',
        'ip_location','user_id', 'nickname', 'gender')

@admin.register(WeiboNotes)
class WeiboNotesAdmin(ImportExportModelAdmin):
    list_display = (
        'note_id', 'content', 'create_date_time', 'liked_count', 'comments_count', 'shared_count',
        'ip_location','user_id', 'nickname', 'gender')
    search_fields = ('content', 'nickname')
    resource_class = WeiboNotesResource

class WeiboNotesIndexResource(resources.ModelResource):
    class Meta:
        model = WeiboNoteIndex
        export_order = ('note_keyword', 'note_doclist')

@admin.register(WeiboNoteIndex)
class WeiboNoteIndexAdmin(ImportExportModelAdmin):
    list_display = ('note_keyword', 'note_doclist')
    search_fields = ('note_keyword',)
    resource_class = WeiboNotesIndexResource


