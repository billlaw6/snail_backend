import urllib.request
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(['GET', 'POST'])
def get_express_info(request, *args, **kwargs):
    print(request.data)
    company = request.data['company']
    postId = request.data['postId']
    url = "http://www.kuaidi100.com/query?type=%s&postid=%s" % (company, postId)
    print(url)
    res = urllib.request.urlopen(url)  # 打开链接，请求快递数据
    content = res.read().decode("utf8")
    jsonObj = json.loads(content)
    return Response(jsonObj, status.HTTP_201_CREATED)
