from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView

from .models import Job, Citys, JobTypes, Resume
from django.template import loader
# Create your views here.

def joblist(request):
    job_list = Job.objects.order_by('job_type')

    context = {'job_list': job_list}

    for job in job_list:
        #将choice类型装换为字符串
        job.city_name = Citys[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]


    return render(request,'joblist.html',context)

def detail(request,job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Citys[job.job_city][1]

    except:
        raise Http404("Job does not exist")

    return render(request,'job.html',{'job':job})

class ResumeCreateView(LoginRequiredMixin, CreateView):
    """    简历职位页面  """
    template_name = 'resume_form1.html'
    success_url = '/joblist/'
    model = Resume
    fields = ["username", "city", "phone",
        "email", "apply_position", "gender",
        "bachelor_school", "master_school", "major", "degree", "picture", "attachment",
        "candidate_introduction", "work_experience", "project_experience"]

    ### 从 URL 请求参数带入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    #简历和当前用户关联
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    '''def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form}) '''

class ResumeDetailView(DetailView):
    #简历详情页
    model = Resume
    template_name = 'resume_detail.html'
