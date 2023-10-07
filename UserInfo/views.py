from django.shortcuts import render, redirect,HttpResponse
from UserAuth.models import User
import os
from django.conf import settings
# Create your views here.
def index(request):
    name = request.session.get("UserInfo")
    context = {"username": name}
    return render(request, "UserInfo/index.html", context)
def resume(request):
    return 1
def apply(request):
    return 1
def account(request):
    return 1
def image_upload(request):
    if request.method == 'POST':
       upload_image = request.FILES['upload']
       # 获取上传文件的后缀名
       file_extension = os.path.splitext(upload_image.name)[1]
       # 这里对文件后缀名进行检验
       white_list = {'.jpg', '.png'}
       print(file_extension)
       if file_extension  not in white_list:
           return HttpResponse('你上传的文件格式不对')
       save_path =  os.path.join(settings.MEDIA_ROOT,str(request.session['UserInfo'].get("id")) + file_extension)
       print(save_path)
       # 保存文件到指定位置
       with open(save_path, 'wb') as file:
           for chunk in upload_image.chunks():
               file.write(chunk)
       return HttpResponse('头像上传成功')
    else:
        return HttpResponse('头像上传失败')
def modify(request):
    # 获取当前用户数据行
    query_set = User.objects.filter(id=request.session['UserInfo'].get("id"))
    # 正常来说根据id查表应该查询出唯一的用户，这里作检查
    if len(query_set) != 1:
        return HttpResponse("不合法的身份")
    # 获取用户数据
    obj = query_set.first()
    user_info = {"id": request.session['UserInfo'].get("id"),
                 "username": obj.username,
                 "mobile_phone": obj.mobile_phone,
                 "gender": obj.gender,
                 "email": obj.email,
                 "edu_ground": obj.edu_ground,
                 "school": obj.school,
                 "major": obj.major,
                 "excepting_position": obj.excepting_position,
                 "excepting_location": obj.excepting_location
                 }
    context = {
        'userinfo': user_info
    }
    return render(request,"UserInfo/userinfo_modify.html",context)
def info(request):
    if request.method == "GET":
        # 查询并返回数据
        query_set = User.objects.filter(id=request.session["UserInfo"].get("id"))
        # 获取用户数据
        obj = query_set.first()
        user_info = {"id": request.session['UserInfo'].get("id"),
                     "username": obj.username,
                     "mobile_phone": obj.mobile_phone,
                     "gender": obj.gender,
                     "email": obj.email,
                     "edu_ground": obj.edu_ground,
                     "school": obj.school,
                     "major": obj.major,
                     "excepting_position": obj.excepting_position,
                     "excepting_location": obj.excepting_location
                     }
        return render(request, "UserInfo/userinfo.html", context=user_info)
        # else POST
    data = request.POST
    fields = ['username', 'mobile_phone', 'gender', 'email',
              'edu_ground', 'school', 'major', 'excepting_position', 'excepting_location']
    new_info = {}
    # 获取当前用户数据行
    query_set = User.objects.filter(id=request.session['UserInfo'].get("id"))
    # 正常来说根据id查表应该查询出唯一的用户，这里作检查
    if len(query_set) != 1:
        return HttpResponse("不合法的身份")
    # 获取用户数据
    obj = query_set.first()
    for field in fields:
        setattr(obj, field, data.get(field))
    user_info = {"id":request.session['UserInfo'].get("id"),
                 "username": obj.username,
                 "mobile_phone": obj.mobile_phone,
                 "gender": obj.gender,
                 "email": obj.email,
                 "edu_ground": obj.edu_ground,
                 "school": obj.school,
                 "major": obj.major,
                 "excepting_position": obj.excepting_position,
                 "excepting_location": obj.excepting_location
                 }
    return render(request, "UserInfo/userinfo.html", context=user_info)
