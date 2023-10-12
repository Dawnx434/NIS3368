from django.urls import path

from PublishPosition import views

"""
should include:
/list   展示列表
view/<int: nid>/    查看编号为nid的岗位详情
"""
urlpatterns = [
    path("list/", views.position_list),
    path("view/<int:nid>/", views.view_position_detail),
]
