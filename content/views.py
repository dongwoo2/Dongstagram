from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed
import os
from Dongstagram.settings import MEDIA_ROOT

# Create your views here.
class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id')

        return render(request,"Dongstagram/main.html",{"feed_list":feed_list})


class UploadFeed(APIView):
    def post(self, request):

        # 파일을 불러오는 거
        file = request.FILES['file']

        uuid_name = uuid4().hex # 이미지 파일의 경우 특수문자 한글 막 뒤죽박죽하게 섞여있다 그것을 영어와 숫자로만 적힌 고유id값으로 만들어준다
        save_path = os.path.join(MEDIA_ROOT, uuid_name)# 경로지정 경로를 join 미디어루트 경로에 uuid_name을 추가 즉 media/uuid_name 이렇게 지정을 하겠다는 뜻 미디어 폴더에 uuid_name으로 고유값이 만들어진 애까지 지정

        with open(save_path, 'wb+') as destination: # 실제로 파일을 저장하는 부분
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        Feed.objects.create(image=image,content=content,user_id=user_id,profile_image=profile_image,like_count=0)
        return Response(status=200)