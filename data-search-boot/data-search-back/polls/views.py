from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import random
from polls.models import Account 

def test(request):
    response = JsonResponse({"talk": "helloworld"})
    return response 

def query_by_QQNum(request):
    
    dict_group = []
  
    
    try:
        # 获取查询的值
        index = request.POST.get('index')
        
        # 得到查询的结果
        accounts = Account.objects.filter(QQNum__icontains=index)
        for account in accounts:
            dict_group.append({
                    'QQNum': account.QQNum,
                    'Nick': account.Nick,
                    'Age': account.Age,
                    'Gender': account.Gender,
                    'Auth': account.Auth,
                    'QunNum': account.QunNum
                })
                
    except Account.DoesNotExist:
        response = JsonResponse(dict_group, safe=False)
        return response        
    # 返回一个json
    else:
        response = JsonResponse(dict_group, safe=False)
        return response

def query_by_Nick(request):
    # 获取查询的值
    index = request.POST.get('index')
    # 得到查询的结果
    accounts = Account.objects.filter(Nick__icontains=index)
    accounts_groups = []
    for account in accounts:
        dict_group = {
            'QQNum': account.QQNum,
            'Nick': account.Nick,
            'Age': account.Age,
            'Gender': account.Gender,
            'Auth': account.Auth,
            'QunNum': account.QunNum
        }
        accounts_groups.append(dict_group)
    # 返回一个json(不是列表格式的)
    response = JsonResponse(accounts_groups, safe=False)
    return response