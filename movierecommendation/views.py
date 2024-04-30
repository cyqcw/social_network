import base64
from io import BytesIO

from django.shortcuts import render
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from sklearn.decomposition import PCA

from movierecommendation.models import DoubanMovie, DoubanMovieIndex, WeiboNotes, WeiboNoteIndex
from django.http import HttpResponse, JsonResponse
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


# 定义微博页面
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
            # 获取所有微博的文本属性用于索引
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
                # 记录关键词在微博数据中出现的词频
                keywordCount = {}
                unique_keywords = set(keywordlist)
                for keyword in unique_keywords:
                    keywordCount[keyword] = keywordlist.count(keyword)
                print("keywordCount = ", keywordCount)

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
                print("list = ", temp, "key", term)
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


import json
import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

from time import *
def weiboSearchIndex(request):
    start_time=time()
    print("request = ", request, "keyword = ", request.GET['keyword'], "method = ", request.method)
    res = {
        'status': 404,
        'text': 'Unknown request!'
    }
    if request.method == 'GET':
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
            result = list(WeiboNotes.objects.filter(id__in=idLst).values())
            print(len(result), time()-start_time)
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




# 词性标注
import jieba
import jieba.posseg as psg

# 扩展词性到颜色的映射
color_map = {
    'n': 'yellow',    # 名词
    'v': 'green',     # 动词
    'a': 'grey',     # 形容词
    'ad': 'orange',  # 副词
    'r': 'white',   # 代词
    'ns': 'pink',    # 地名
}

# 定义词性标注请求链接
@csrf_exempt
def posannotation(request):
    if request.method == 'GET':
        print("keyword = ", request.GET['id'], "method = ", request.method)
        # 获取请求参数
        note_id = request.GET.get('id')
        if note_id:
            try:
                # 从数据库中获取微博数据
                weibo_note = WeiboNotes.objects.get(id=note_id)
                original_content = weibo_note.content

                # 读出停用词
                stopwords = []
                static_filepath = os.path.join(settings.STATIC_ROOT, 'refs')
                file_path = os.path.join(static_filepath, 'stopwords.txt')
                for word in open(file_path, encoding='utf-8'):
                    stopwords.append(word.strip())

                # 进行词性标注
                seg_list = psg.cut(original_content)

                # 构建标注后的HTML文本
                annotated_text = ''
                for word, flag in seg_list:
                    if flag in color_map and word not in stopwords:
                        annotated_text += f'<span style="background-color: {color_map[flag]};">{word}</span>'
                    else:
                        annotated_text += word
                # 准备响应数据
                response_data = {
                    'id': note_id,
                    'content': annotated_text,
                    'create_date_time': weibo_note.create_date_time,
                    'nickname': weibo_note.nickname,
                    'ip_location': weibo_note.ip_location,
                    'gender': weibo_note.gender,
                }

                res = {
                    'status': 200,
                    'data': response_data
                }
            except WeiboNotes.DoesNotExist:
                res = {
                    'status': 404,
                    'data': 'Note not found!'
                }
        else:
            res = { 'status': 400, 'data': 'Invalid request, missing note ID.' }
    else:
        res = {
            'status': 405,
            'data': 'Method Not Allowed'
        }
    return JsonResponse(res)


import spacy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

# 加载spacy模型，这里假设使用了jieba插件，但具体可能需要根据实际安装的模型调整
nlp = spacy.load('zh_core_web_sm')

# 定义颜色映射，根据实体类型设定字体颜色
text_color_map = {
    'PER': 'red',  # 人名
    'LOC': 'blue',  # 地名
    'ORG': 'green',  # 机构名
}

@csrf_exempt
def nerannotation(request):
    if request.method == 'GET':
        note_id = request.GET.get('id')
        if note_id:
            try:
                weibo_note = WeiboNotes.objects.get(id=note_id)
                original_content = weibo_note.content
                # 使用spacy进行实体识别
                doc = nlp(original_content)

                # 构建标注后的HTML文本
                annotated_text = original_content
                for ent in doc.ents:
                    # 使用CSS样式更改字体颜色
                    annotated_text = annotated_text.replace(
                        str(ent),
                        f'<span style="color: {text_color_map.get(ent.label_, "black")};">{str(ent)}</span>'
                    )

                response_data = {
                    'id': note_id,
                    'content': annotated_text,
                    'create_date_time': weibo_note.create_date_time,
                    'nickname': weibo_note.nickname,
                    'ip_location': weibo_note.ip_location,
                    'gender': weibo_note.gender,
                }

                res = {
                    'status': 200,
                    'data': response_data
                }
            except WeiboNotes.DoesNotExist:
                res = {
                    'status': 404,
                    'data': 'Note not found!'
                }
        else:
            res = {'status': 400, 'data': 'Invalid request, missing note ID.'}
    else:
        res = {
            'status': 405,
            'data': 'Method Not Allowed'
        }
    return JsonResponse(res)





#加载Python库
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba.analyse

# 定义挖掘页面.
def doubanClassification(request):
    # 数据预处理
    # 获取所有电影的文本并进行中文分词与预处理
    movie_list = DoubanMovie.objects.values('id', 'movie_title', 'movie_description')
    movie_set = []
    for movie in movie_list:
        text = movie['movie_title'] + movie['movie_description']
        # 正则表达式去除非文字和数字的字符
        movie_text = re.sub(r'[^\w]+', '', text.strip())
        movie_set.append(movie_text)

    # 初始化停用词列表
    # 注意：从网上下载一个较为全面完整的stopwords.txt用于本次任务。此处只是一个简单的示例文件
    stopwords = []
    static_filepath = os.path.join(settings.STATIC_ROOT, 'refs')
    file_path = os.path.join(static_filepath, 'stopwords.txt')
    for word in open(file_path, encoding='utf-8'):
        stopwords.append(word.strip())

    # 定义分词函数
    def tokenizer(s):
        words = []
        cut = jieba.cut(s)
        for word in cut:
            words.append(word)
        return words

    # 创建一个向量计数器对象
    count = CountVectorizer(tokenizer=tokenizer, stop_words=list(stopwords))
    countvector = count.fit_transform(movie_set).toarray()

    # 此处的主成分维度我们人为设定为2，对于属性较少的数据集，属于常规会选择的维度数，后面也会看到，这个也是出于可以可视化的需求
    new_pca = PCA(n_components=2)
    # 将设置了维数的模型作用到标准化后的数据集并输出查看
    X = new_pca.fit_transform(countvector)

    # K-means聚类建模
    # 运行KMeans聚类算法
    # 此处指定K=3
    estimator = KMeans(n_clusters=3)
    estimator.fit(X)
    # 获取聚类标签
    label_pred = estimator.labels_

    #绘制k-means结果
    plt.switch_backend('Agg')
    x0 = X[label_pred == 0]
    x1 = X[label_pred == 1]
    x2 = X[label_pred == 2]
    plt.scatter(x0[:, 0], x0[:, 1], c = "red", marker='o', label='label0')
    plt.scatter(x1[:, 0], x1[:, 1], c = "green", marker='*', label='label1')
    plt.scatter(x2[:, 0], x2[:, 1], c = "blue", marker='+', label='label2')
    plt.legend(loc=2)
    plt.title("KMeans聚类结果显示")
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,'+str(data)
    plt.close()

    clusters = ' '.join(movie_set)
    # 提取clusters的主题关键词
    kw1 = jieba.analyse.textrank(clusters, topK=50, withWeight=True, allowPOS=('ns', 'n'))
    words_frequence = {x[0]: x[1] for x in kw1}
    file_bg_path = os.path.join(static_filepath, 'cat.jpg')
    backgroud_Image = plt.imread(file_bg_path)
    # 若是有中文的话，font_path必须添加，不然会出现乱码，不出现汉字
    # simsun.ttc为汉字编码文件，可以从本地windows系统找一个汉字编码文件上传， 如C:\\Windows\Fonts下有许多汉字编码文件
    file_font_path = os.path.join(static_filepath, 'simsun.ttc')
    wordcloud = WordCloud(font_path=file_font_path, mask=backgroud_Image, repeat=True, background_color='white')
    wordcloud = wordcloud.fit_words(words_frequence)
    plt.imshow(wordcloud)
    plt.axis("off")
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    cloud_data = base64.encodebytes(sio.getvalue()).decode()
    cloud_src = 'data:image/png;base64,' + str(cloud_data)
    plt.close()

    # 保持图片，其他结果图也可以参照此方法先保存图片，再从前端读取图片路径进行显示
    file_img_path = os.path.join(static_filepath, 'wordcloudcluster.jpg')
    wordcloud.to_file(file_img_path)

    image_list = []
    image_list.append(cloud_src)

    # image_list: 聚类结果每一类的词云图
    return render(request, 'doubanClassification.html', {
            'image_cluters': src,
            'cluster_list': image_list
        })






