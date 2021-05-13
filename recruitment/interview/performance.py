import time
import logging

logger = logging.getLogger(__name__)

#用来实现自定义中间件
#记录用户URl传来的参数并记录处理时间

def perfromance_logger_middleware(get_response):
    #get_response是必须存在的参数

    def middlemare(request):
        start_time = time.time()
        response = get_response(request)
        duration =time.time()-start_time

        #设置后能够通过浏览器的开发工具看到该参数
        response["X-Page-Duration-as"] = int(duration*1000)
        logger.info("%s %s %s",duration,request.path,request.GET.dict())
        return response

    return middlemare