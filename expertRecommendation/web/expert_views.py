# -*- coding: utf-8 -*-
# Create your views here.
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from web.models import *
import Levenshtein

def list_experts(request,page):
    user = request.user
    if request.user.is_authenticated():
        page = int(page)
        expertlist = Expert.objects.exclude(keywords='').order_by('expertID')[(page-1)*100:page*100]
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
            #print expert_friend_list
            match_degree = 0
            match_count = 0
            for k1 in keyword_list:
                max_match = 0
                match_count += 1
                for k2 in expert_keyword_list:
                    k2 = k2.encode('utf-8')
                    #match = Levenshtein.ratio(k1,k2)
                    match = 0
                    if(k1  == k2):
                        match = 1
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
                        print a1
                        print a2
                if is_match:
                    relative_degree += 1
                    print relative_degree
                relative_count += 1
                print relative_count

            if match_count == 0:
                return HttpResponse("没有关键词")
            if relative_count == 0:
                relative_degree = 0
                relative_count = 1
            else:
                match_degree = float(match_degree)/float(match_count)*100
                relative_degree = float(relative_degree)/float(relative_count)*100
                return HttpResponse("匹配度：{0}%<br/>排斥度：{1}%<br/>推荐度：{2}%".format(match_degree,relative_degree,match_degree-relative_degree))
        except:
            return HttpResponse("参数错误")
    else:
        return HttpResponse(0)
@csrf_protect
def match_view(request):
    if request.user.is_authenticated():
        user = request.user
        return render_to_response('expert/match.html',locals(),context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")

def group_match(request):
    if request.user.is_authenticated():
        try:
            itemNumber = request.POST['itemnumber']
            count = 1
            items = []
            while(count <= int(itemNumber)):
                keywords = request.POST['keyword'+count.__str__()]
                keywords = keywords.split(' ')
                authors = request.POST['author'+count.__str__()]
                authors = authors.split(' ')
                items.append({'keywords':keywords,'authors':authors})
                count += 1
            experts = Expert.objects.exclude(keywords = '').order_by('expertID')[0:100]
            expert_list = []
            expert_count = 0
            for e in experts:
                papers = Paper.objects.filter(expertID = e.expertID)
                expert_friend_list = []
                #expert_count += 1
                #print expert_count
                for paper in papers:
                    friend_str = paper.authorlist.encode('utf-8')
                    friend_list =   friend_str.split(',')
                    expert_friend_list.extend(friend_list)
                expert_keyword_list = e.keywords.split(' ')
                expert_list.append({'expertID':e.expertID,'expert_friend_list':expert_friend_list,'expert_keyword_list':expert_keyword_list})
                    #get match degree

            item_expert_rectangle = []
            for t in items:
                item_expert_list = {}
                for s in expert_list:
                    match_count = 0
                    match_degree = 0
                    for k1 in t['keywords']:
                        match_count += 1
                        K_match = False
                        for k2 in s['expert_keyword_list']:
                            if k1 == k2:K_match = True
                        if K_match:match_degree += 1
                    match_degree = match_degree/match_count
                    relative_count = 0
                    relatvie_degree = 0
                    for e1 in t['authors']:
                        relative_count += 1
                        E_match = False
                        for e2 in s['expert_friend_list']:
                            if e1 == e2:E_match = True
                        if E_match:relatvie_degree += 1
                    relatvie_degree = relatvie_degree/relative_count

                    match_degree = match_degree - relatvie_degree
                    if (match_degree > 0):
                        item_expert_list[s['expertID']] = match_degree
                item_expert_rectangle.append(item_expert_list)


                    #end get match degree
            return HttpResponse("匹配成功")
        except:
            return HttpResponse("参数错误")
    else:
        return HttpResponse(0)
