from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Reply, Like, Bookmark
from user.models import User
import os
from Dongstagram.settings import MEDIA_ROOT

# Create your views here.
class Main(APIView):
    def get(self, request):
        feed_object_list = Feed.objects.all().order_by('-id')
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id) # 그 피드 하나에 적힌 댓글 목록을 불러올 수 있다.
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(
                    reply_content=reply.reply_content,
                    nickname=user.nickname,
                ))
            feed_list.append(dict(
                                  id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=feed.like_count,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname, # 실시간 데이터 반영
                                  reply_list=reply_list
                                  ))

#        print('로그인한 사용자:', request.session['email'])
        email = request.session.get('email', None)

        if email is None: # 로그인을 안한 상태로 접속했을 때
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:# 이메일 주소는 있는데 우리 회원이 아닐 때
            return render(request, "user/login.html") # 그러면 로그인 다시해

        return render(request,"Dongstagram/main.html",{"feed_list":feed_list, "user" : user})


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
        email = request.session.get('email', None) # 세션이 있다는거는 로그인한 증거니까 세션에서 가져오고

        Feed.objects.create(image=image,content=content,email=email,like_count=0)
        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None: # 로그인을 안한 상태로 접속했을 때
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:# 이메일 주소는 있는데 우리 회원이 아닐 때
            return render(request, "user/login.html") # 그러면 로그인 다시해

        return render(request, "content/profile.html", {"user":user})


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id,reply_content=reply_content, email=email)

        return Response(status=200)