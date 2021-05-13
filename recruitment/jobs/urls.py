from django.conf.urls import url
from django.urls import path

from .views import joblist,detail,ResumeCreateView,ResumeDetailView

urlpatterns = [
    #职位列表
    url(r"^joblist/",joblist,name="joblist"),

    #职位详情
    url(r'^job/(?P<job_id>\d+)/$',detail,name='detail'),

    #首页自动跳转到职位列表
    url(r'^$',joblist,name='name'),

    #提交简历
    path('resume/add/',ResumeCreateView.as_view(),name = 'resume-add'),

    #简历详情页
    path('resume/<int:pk>/',ResumeDetailView.as_view(),name = 'resume-detail'),
]