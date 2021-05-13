from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponse
import csv
import datetime

from django.utils.safestring import mark_safe

from .models import Candidate
import logging
from .candidate_fieldset import default_fieldsets,default_fieldsets_first,default_fieldsets_second


# Register your models here.
from jobs.models import Resume

logger = logging.getLogger(__name__)
#导出的范围
exportable_fields = ('username','city','bachelor_school','first_score','first_result','first_interviewer_user',
        'second_result','second_interviewer_user','hr_score','hr_result',)

def export_model_as_csv(modeladmin,request,queryset):
    #编写函数，实现将用户信息导出的功能
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment;filename = recruitment-candidates-list-%s.csv'%(
        datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )
    #写入表头
    write = csv.writer(response)
    write.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )
    for obj in queryset:
        #单行的数据
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        write.writerow(csv_line_values)

    logger.info("%s exported %s candidate recoeds" %(request.user,len(queryset)))
    return response

export_model_as_csv.short_description = u'导出为CSV文件'
export_model_as_csv.allowed_permissions = ('export',)



class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator','created_time','modified_date')

    #展示字段
    #除get_resume是定义的函数外，其余字段都是真实实体中的字段
    list_display = (
        'username','city','bachelor_school','get_resume','first_score','first_result','first_interviewer_user',
        'second_result','second_interviewer_user','hr_score','hr_result','last_editor'
    )

    def get_resume(self,obj):
        #list_display 定义了列表展示，但是不仅可以引用真实的字段，也可以引用方法
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone = obj.phone)
        if resumes and len(resumes)>0:
            return mark_safe(u'<a href = "/resume/%s" target = "_blank">%s</a' % (resumes[0].id,"查看简历"))

        return ""

    get_resume.short_description = u'查看简历'
    get_resume.allow_tags =True
    #额外动作
    actions = [export_model_as_csv,]

    # 当前用户是否有到处权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    #筛选条件
    list_filter = ('city','first_result','second_result','hr_result','first_interviewer_user','second_interviewer_user')

    #搜索属性
    search_fields = ('username','phone','email','bachelor_school')

    #默认排序
    ordering = ('hr_result','second_result','first_result')

    #在列表页直接编辑,可以分配面试官
    default_list_editable = ('first_interviewer_user','second_interviewer_user')

    #实现方法能够使得只有HR和超级管理员能够实现在列表页进行编辑
    def get_list_editable(self,request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'HR' in group_names:
            return self.default_list_editable

        return ()

    def get_changelist_instance(self, request):
        #django中没有对应的方法来实现对列表页的编辑
        #覆盖父类中的方法使得能够实现该功能
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin,self).get_changelist_instance(request)


    #设置只读字段，对所有用户如此
    #readonly_fields = ('first_interviewer_user','second_interviewer_user')

    #获取群组
    def get_group_names(self,user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)

        return group_names

    #对可读字段进行设置，HR用户可以进行使用
    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("insterviewer is user for %s" %request.user.username)
            return ('first_interviewer_user','second_interviewer_user')
        return ()


    # 一面面试官仅填写一面反馈， 二面面试官可以填写二面反馈
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return default_fieldsets_second
        return default_fieldsets

    #数据集权限
    # 对于非管理员，非HR，获取自己是一面面试官或者二面面试官的候选人集合:s
    def get_queryset(self, request):  # show data only owned by the user
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'HR' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user))

    # list_editable = ('first_interviewer_user','second_interviewer_user',)


admin.site.register(Candidate,CandidateAdmin)