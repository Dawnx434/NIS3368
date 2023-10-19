from django.shortcuts import render, HttpResponse, redirect
from django.utils.safestring import mark_safe
import markdown

from PublishPosition.models import Position
from UserAuth.models import User
from PublishPosition.utils.forms.MyForm import PublishPositionForm

from PublishPosition.utils.provincelist import province_dictionary
from PublishPosition.utils.district import district_dictionary
from PublishPosition.utils.check_position_form import check_publish_position_form

import os
from django.conf import settings
import re

# Create your views here.
def position_list(request):
    """返回职位列表"""
    # get query condition: Page and PageSize
    try:
        page = 1 if not request.GET.get('Page') else int(request.GET.get('Page'))
        pagesize = 20 if not request.GET.get('PageSize') else int(request.GET.get('PageSize'))
    except ValueError as e:
        return HttpResponse("异常的查询参数")

    # get list
    query_set = Position.objects.filter(published_state=1)

    # filter according to query params
    query_set = query_set[(page - 1) * pagesize: page * pagesize - 1]

    context = {
        'query_set': query_set

    }
    return render(request, 'PublishPosition/position_list.html', context)


def view_position_detail(request, nid):
    """展示岗位的详细信息"""
    obj = Position.objects.filter(id=nid, published_state=1)  # 1 表示已发布
    # 判空
    if not obj:
        return HttpResponse("不存在的招聘信息或未开放的招聘信息")

    position = obj.first()
    context = {
        "user_id": request.session.get("UserInfo")['id'],
        "position_id": position.id,
        "position_name": position.position_name,
        "salary": position.salary,
        "summary": position.summary,
        # XSS alert; need fix
        "detail": mark_safe(markdown.markdown(position.detail,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                    ])),
        # "detail": position.detail,
        "HR": position.HR,
        "district": position.get_district_display(),
    }

    return render(request, "PublishPosition/position_detail.html", context)


def publish_position(request):
    # Publish Position理应只能HR身份登录，因此优先校验是否是HR身份
    # 获取当前登录用户信息
    user_obj = User.objects.filter(id=request.session.get("UserInfo")['id']).first()
    # 检查发布职位者的身份是否为HR
    if user_obj.identity != 2:
        # 当前登录用户非HR身份
        return HttpResponse("请使用HR身份登录！")

    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    file_names = os.listdir(settings.MEDIA_ROOT)
    matching_files = []
    for file_name in file_names:
        if pattern.match(file_name):
            matching_files.append(file_name)
    # 没有上传就用默认的
    if not matching_files:
        matching_files.append('default.jpeg')
    # # else POST
    # data = request.POST
    # fields = ['username', 'mobile_phone', 'gender', 'email',
    #           'edu_ground', 'school', 'major', 'excepting_position', 'excepting_location']
    # # 获取当前用户数据行
    # query_set = User.objects.filter(id=request.session['UserInfo'].get("id"))
    # # 正常来说根据id查表应该查询出唯一的用户，这里作检查
    # if len(query_set) != 1:
    #     return HttpResponse("不合法的身份")
    # # 获取用户数据
    # obj = query_set.first()
    # for field in fields:
    #     setattr(obj, field, data.get(field))
    # obj.save()
    # user_info = {"id": request.session['UserInfo'].get("id"),
    #              "username": obj.username,
    #              "mobile_phone": obj.mobile_phone,
    #              "gender": obj.get_gender_display(),
    #              "email": obj.email,
    #              "edu_ground": obj.edu_ground,
    #              "school": obj.school,
    #              "major": obj.major,
    #              "excepting_position": obj.excepting_position,
    #              "excepting_location": obj.excepting_location,
    #              "matching_files": matching_files[0],
    #              }
    # return render(request, "UserInfo/userinfo.html", context=user_info)

    if request.method == 'GET':
        form = PublishPositionForm()
        context = {
            'district_dictionary': district_dictionary,
            "matching_files": matching_files[0],
        }
        return render(request, "PublishPosition/position_publish.html", context)

    # else POST
    data_dict = {}
    error_dict = {}
    for field in ['position_name', 'salary', 'summary', 'detail', 'district', 'published_state']:
        data_dict[field] = request.POST.get(field)

    print(data_dict['detail'])
    # 补充字段
    data_dict['HR'] = user_obj

    # 字段校验
    data_dict, error_dict, check_passed_flag = check_publish_position_form(data_dict)

    print(check_passed_flag)
    if not check_passed_flag:
        # 未通过检查
        context = {
            'district_dictionary': district_dictionary,
            'data_dict': data_dict,
            'error_dict': error_dict
        }
        return render(request, "PublishPosition/position_publish.html", context)

    # 通过字段检查
    Position.objects.create(**data_dict)
    return redirect('/position/list/')


def modify_position(request, nid):
    query_set = Position.objects.filter(id=nid)
    if not query_set:
        return HttpResponse("不存在的岗位信息！")
    # 获取目标岗位对象
    position_obj = query_set.first()
    # 获取当前登录用户信息
    user_obj = User.objects.filter(id=request.session.get("UserInfo")['id']).first()
    # 检查发布职位者的身份是否为HR
    if user_obj.identity != 2:
        # 当前登录用户非HR身份
        return HttpResponse("请使用HR身份登录！")
    # 检查当前用户是否具有编辑权限
    if request.session.get("UserInfo")['id'] != position_obj.HR_id:
        return HttpResponse("你不具有对当前岗位修改的权限")

    if request.method == 'GET':
        # 获取属性内容['position_name', 'salary', 'summary', 'detail', 'province', 'published_state']
        data_dict = {
            'position_name': position_obj.position_name,
            'salary': position_obj.salary,
            'summary': position_obj.summary,
            'detail': position_obj.detail,
            'district': position_obj.district,
            'published_state': position_obj.published_state
        }
        context = {
            'district_dictionary': district_dictionary,
            'data_dict': data_dict
        }

        return render(request, "PublishPosition/position_modify.html", context)

    # else POST
    data_dict = {}
    error_dict = {}
    # 提取数据
    for field in ['position_name', 'salary', 'summary', 'detail', 'district', 'published_state']:
        data_dict[field] = request.POST.get(field)
    # 检查字段
    data_dict, error_dict, check_passed_flag = check_publish_position_form(data_dict)
    if not check_passed_flag:
        # 未通过检查
        context = {
            'district_dictionary': district_dictionary,
            'data_dict': data_dict,
            'error_dict': error_dict
        }
        return render(request, "PublishPosition/position_modify.html", context)

    # 通过字段检查
    query_set.update(**data_dict)
    return redirect('/position/list/')
