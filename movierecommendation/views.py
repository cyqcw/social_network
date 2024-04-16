from django.shortcuts import render
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from movierecommendation.models import DoubanMovie, DoubanMovieIndex, WeiboNotes, WeiboNoteIndex
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import jieba
import re
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from fuzzywuzzy import fuzz


# 定义推荐页面
def doubanRecommendation(request):
    movie_list = DoubanMovie.objects.all().order_by('id')  # 取出DoubanMoview表所有数据并排序
    paginator = Paginator(movie_list, 3)  # 3是每页显示的数量，把数据库取出的数据生成paginator对象，并指定每页显示的数量
    page = request.GET.get('page')  # 从查询字符串获取page的当前页数
    data_list = []
    if page:  # 判断：获取当前页码的数据集，这样在模版就可以针对当前的数据集进行展示
        data_list = paginator.page(page).object_list
    else:
        data_list = paginator.page(1).object_list
    try:  # 实现分页对象，分别判断当页码存在/不存在的情况，返回当前页码对象
        page_object = paginator.page(page)
    except PageNotAnInteger:
        page_object = paginator.page(1)
    except EmptyPage:
        page_object = paginator.page(paginator.num_pages)
    return render(request, 'doubanRecommendation.html', {
        'page_object': page_object,
        'data_list': data_list
    })


# 定义索引请求链接
@csrf_exempt
def buildindex(request):
    res = {
        'status': 404,
        'text': 'Unknown request!'
    }
    if request.method == 'POST':
        name = request.POST['id']
        if name == 'submit2index':
            # 初始化停用词列表
            stopwords = []
            static_filepath = os.path.join(settings.STATIC_ROOT, 'refs')
            file_path = os.path.join(static_filepath, 'stopwords.txt')
            for word in open(file_path, encoding='utf-8'):
                stopwords.append(word.strip())
            # 获取所有电影的文本属性用于索引
            movie_list = DoubanMovie.objects.values('id', 'movie_title', 'movie_keywords', 'movie_description')
            all_keywords = []
            movie_set = dict()
            for movie in movie_list:
                movie_id = movie['id']
                text = movie['movie_title'] + movie['movie_keywords'] + movie['movie_description']
                # 正则表达式去除非文字和数字的字符
                movie_text = re.sub(r'[^\w]+', '', text.strip())
                cut_text = jieba.cut(movie_text, cut_all=False)
                keywordlist = []
                for word in cut_text:
                    # 此处去停用词
                    if word not in stopwords:
                        keywordlist.append(word)
                all_keywords.extend(keywordlist)
                movie_set[movie_id] = keywordlist
            # 利用set删除重复keywords
            set_all_keywords = set(all_keywords)
            # 建立倒排索引
            for term in set_all_keywords:
                temp = []
                for m_id in movie_set.keys():
                    cut_text = movie_set[m_id]
                    if term in cut_text:
                        temp.append(m_id)
                # 存储索引到数据库
                try:
                    exist_list = DoubanMovieIndex.objects.get(movie_keyword=term)
                    exist_list.movie_doclist = json.dumps(temp)
                    exist_list.save()
                except ObjectDoesNotExist:
                    new_list = DoubanMovieIndex(movie_keyword=term, movie_doclist=json.dumps(temp))
                    new_list.save()
            res = {
                'status': 200,
                'text': 'Index successfully!'
            }
    return HttpResponse(json.dumps(res), content_type='application/json')


# 定义检索请求链接.
def searchindex(request):
    res = {
        'status': 404,
        'text': 'Unknown request!'
    }
    if request.method == 'GET':
        name = request.GET['id']
        if name == 'submit2search':
            try:
                # 获取前端的关键词
                keyword = request.GET['keyword']
                # 精确匹配索引关键词
                # 如何实现模糊匹配？
                invertedindex_rec = DoubanMovieIndex.objects.get(movie_keyword=keyword)
                # 将文档列表字符串转化成数组
                jsonDec = json.decoder.JSONDecoder()
                result = jsonDec.decode(invertedindex_rec.movie_doclist)
                # 查询电影ID在数组内的数据
                result_queryset = DoubanMovie.objects.filter(id__in=result).values()
                if result_queryset:
                    res = {
                        'status': 200,
                        'text': list(result_queryset)
                    }
                else:
                    res = {
                        'status': 201,
                        'text': 'No result!'
                    }
            except ObjectDoesNotExist:
                res = {
                    'status': 201,
                    'text': 'No result!'
                }
    return HttpResponse(json.dumps(res), content_type='application/json')


# 定义微博评论页面
def weiboRecommendation(request):
    note_list = WeiboNotes.objects.all().order_by('id')  # 取出WeiboNotes表所有数据并排序
    paginator = Paginator(note_list, 20)  # 3是每页显示的数量，把数据库取出的数据生成paginator对象，并指定每页显示的数量
    page = request.GET.get('page')  # 从查询字符串获取page的当前页数
    data_list = []
    if page:  # 判断：获取当前页码的数据集，这样在模版就可以针对当前的数据集进行展示
        data_list = paginator.page(page).object_list
    else:
        data_list = paginator.page(1).object_list
    try:  # 实现分页对象，分别判断当页码存在/不存在的情况，返回当前页码对象
        page_object = paginator.page(page)
    except PageNotAnInteger:
        page_object = paginator.page(1)
    except EmptyPage:
        page_object = paginator.page(paginator.num_pages)
    return render(request, 'weiboRecommendation.html', {
        'page_object': page_object,
        'data_list': data_list
    })


# 定义微博索引请求链接
@csrf_exempt
def weibobuildindex(request):
    res = {
        'status': 404,
        'text': 'Unknown request!'
    }
    if request.method == 'POST':
        name = request.POST['id']
        if name == 'weibosubmit2index':
            # 初始化停用词列表
            stopwords = []
            static_filepath = os.path.join(settings.STATIC_ROOT, 'refs')
            file_path = os.path.join(static_filepath, 'stopwords.txt')
            for word in open(file_path, encoding='utf-8'):
                stopwords.append(word.strip())
            print("stopwords = ", stopwords)
            # 获取所有微博评论的文本属性用于索引
            note_list = WeiboNotes.objects.values('id', 'content', 'nickname', 'ip_location')
            print("note_list = ", len(note_list))
            all_keywords = []
            note_set = dict()
            for note in note_list:
                note_id = note['id']
                text = note['content']
                if note['nickname'] != None:
                    text += note['nickname']
                if text == None:
                    continue
                print("text = ", text)
                # 正则表达式去除非文字和数字的字符
                note_text = re.sub(r'[^\w]+', '', text.strip())
                cut_text = jieba.cut(note_text, cut_all=False)
                keywordlist = []
                for word in cut_text:
                    # 此处去停用词
                    if word not in stopwords:
                        keywordlist.append(word)
                all_keywords.extend(keywordlist)
                note_set[note_id] = keywordlist
            # 利用set删除重复keywords
            set_all_keywords = set(all_keywords)
            print("set_all_keywords", set_all_keywords)
            # 建立倒排索引
            for term in set_all_keywords:
                temp = []
                for c_id in note_set.keys():
                    cut_text = note_set[c_id]
                    if term in cut_text:
                        temp.append(c_id)
                print("temp = ", temp, "key", term)
                # 存储索引到数据库
                try:
                    exist_list = WeiboNoteIndex.objects.get(note_keyword=term)
                    exist_list.note_doclist = json.dumps(temp)
                    exist_list.save()
                except ObjectDoesNotExist:
                    new_list = WeiboNoteIndex(note_keyword=term, note_doclist=json.dumps(temp))
                    new_list.save()
            res = {
                'status': 200,
                'text': 'Index successfully!'
            }
    return HttpResponse(json.dumps(res), content_type='application/json')





def calculate_similarity(str1, str2):
    return fuzz.ratio(str1, str2)



from django.db.models import Count

import json
import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

def weiboSearchIndex(request):
    print("request = ", request, "keyword = ", request.GET['keyword'], "method = ", request.method)
    # print("id = ", request.GET['id'])
    res = {
        'status': 404,
        'text': 'Unknown request!'
    }
    if request.method == 'GET':
        # name = request.GET['id']
        # print("name = ", name)
        # if name == 'weibosubmit2search':
        try:
            # Get the user's search query and split it into keywords
            user_keywords = jieba.cut(request.GET['keyword'], cut_all=False)
            print("user_keywords = ", user_keywords)
            # Get all keywords from the inverted index in the database
            db_keywords = WeiboNoteIndex.objects.values_list('note_keyword', flat=True)
            # print("db_keywords = ", db_keywords)
            relevant_keywords = []
            # For each user keyword, calculate the similarity with all db keywords
            for user_keyword in user_keywords:
                for db_keyword in db_keywords:
                    if calculate_similarity(user_keyword, db_keyword) > 70:  # adjust threshold as needed
                        relevant_keywords.append(db_keyword)
            # Get the documents that contain the relevant keywords
            print("relevant_keywords = ", relevant_keywords)
            relevant_docs = WeiboNoteIndex.objects.filter(note_keyword__in=relevant_keywords)
            print("relevant_docs = ", relevant_docs)

            # Count the number of times each keyword appears in each document
            doc_keyword_counts = {}
            for doc in relevant_docs:
                doc_keywords = json.loads(doc.note_doclist)
                for keyword in doc_keywords:
                    if keyword not in doc_keyword_counts:
                        doc_keyword_counts[keyword] = 1
                    else:
                        doc_keyword_counts[keyword] += 1
            docLst=sorted(doc_keyword_counts.items(), key=lambda x: x[1], reverse=True)
            print("docLst = ", docLst)
            idLst=[ i[0] for i in docLst ]
            result=[]
            # for id in idLst:
            #     result_query = WeiboNotes.objects.get(id=id)
            #     print("result_query = ", result_query)
            #     result.append(result_query)
            result = list(WeiboNotes.objects.filter(id__in=idLst).values())
            # print("result_query = ", result_query)
            #
            # results_dict = {obj[id] : obj for obj in result_query}
            # print("results_dict = ", results_dict)
            # result = [results_dict[id] for id in idLst if id in results_dict]
            # print("result = ", result)
            if result:
                res = {
                    'status': 200,
                    'text': result
                }
            else:
                res = {
                    'status': 201,
                    'text': 'No result!'
                }
        except ObjectDoesNotExist:
            res = {
                'status': 201,
                'text': 'No result!'
            }
    return HttpResponse(DateTimeEncoder().encode(res), content_type='application/json')
