# -*- coding: utf-8 -*-
# Create your views here.
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from web.models import *
import Levenshtein

def list_experts(request,page):
    user = request.user
    if request.user.is_authenticated():
        page = int(page)
        expertlist = Expert.objects.all().order_by('expertID')[(page-1)*100:page*100]
        if(page > 0):
            previous_page = page - 1
            page1 = page
            page2 = page + 1
            page3 = page + 2
            page4 = page + 3
            page5 = page + 4
            next_page = page + 5
        else:
            previous_page = page
            page1 = page
            page2 = page + 1
            page3 = page + 2
            page4 = page + 3
            page5 = page + 4
            next_page = page + 5

        return render_to_response('expert/list.html',locals())
    else:
        return HttpResponseRedirect("/")
def search_expert(request):
    user = request.user
    if request.user.is_authenticated():
        try:
            search_name = request.GET['search_name']
            expertlist = Expert.objects.filter(expertName__icontains=search_name).order_by('expertID')[0:100]
        except:
            expertlist = None
        return render_to_response('expert/list.html',locals())
    else:
        return HttpResponseRedirect("/")
def detail(request,expertID):
    if request.user.is_authenticated():
        user = request.user
        try:
            expertID = expertID.encode('utf-8')
            expertID = int(expertID)
            expert = Expert.objects.get(expertID = expertID)
            paper_list = Paper.objects.filter(expertID = expertID)
        except:
            expert = None
            paper_list = None
        return render_to_response('expert/details.html',locals())
    else:
        return HttpResponseRedirect("/")
def getmatch(request,expertID):
    if request.user.is_authenticated():
        try:
            keywords  = request.GET['keywords'].encode('utf-8')
            authorsID  = request.GET['authorsID'].encode('utf-8')
            keyword_list = keywords.split(' ')
            author_list = authorsID.split(' ')

            e = Expert.objects.get(expertID=expertID)
            expert_keywords = e.keywords
            expert_keyword_list = expert_keywords.split(' ')

            papers = Paper.objects.filter(expertID=expertID)
            expert_friend_list = []
            for paper in papers:
                friend_str = paper.authorlist.encode('utf-8')
                friend_list =   friend_str.split(',')
                expert_friend_list.extend(friend_list)
            print expert_friend_list
            match_degree = 0
            match_count = 0
            for k1 in keyword_list:
                max_match = 0
                match_count += 1
                for k2 in expert_keyword_list:
                    k2 = k2.encode('utf-8')
                    match = Levenshtein.ratio(k1,k2)
                    if(match > max_match):
                        max_match = match
                match_degree += max_match
            relative_degree = 0
            relative_count= 0
            for a1 in author_list:
                is_match = False
                for a2 in expert_friend_list:
                    if(a1 == a2):
                        is_match = True
                if is_match:
                    relative_degree += 1
                relative_count += 1

            if match_count == 0:
                return HttpResponse("没有关键词")
            if relative_count == 0:
                relative_degree = 0
                relative_count = 1
            else:
                match_degree = match_degree/match_count*100
                relative_degree = relative_degree/relative_count*100
                return HttpResponse("匹配度：{0}%<br/>相关度：{1}%<br/>推荐度：{2}%".format(match_degree,relative_degree,match_degree-relative_degree))
        except:
            return HttpResponse("参数错误")
    else:
        return HttpResponse(0)