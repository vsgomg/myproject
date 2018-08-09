import json
import redis

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,FormParser

from api import models
from api.utils.response import BaseResponse

# 常量名大写
CONN = redis.Redis(host='192.168.11.128',port=6379)

USER_ID = 1

class ShoppingCarView(ViewSetMixin,APIView):

    def list(self,request,*args,**kwargs):
        ret =  {'code':10000,'data':None,'error':None}

        try:
            # 因为用户会选择多个课程,所以课程信息用列表存放起来
            shopping_car_course_list = []
            # 拼接用户id作为redis的查询关键字
            pattern = settings.LUFFY_SHOPPING_CAR%(USER_ID,'*')

            # 获取redis中用户购物车信息
            user_key_list = CONN.keys(pattern)

            for key in user_key_list:
                temp = {
                    'id':CONN.hget(key,'id').decode('utf8'), # 商品id
                    'name':CONN.hget(key,'name').decode('utf8'), # 商品名字
                    'img':CONN.hget(key,'img').decode('utf8'), # 商品图片
                    'default_price_id':CONN.hget(key,'default_price_id').decode('utf8'), # 默认价格
                    'price_policy_dict':json.loads(CONN.hget(key,'price_policy_dict').decode('utf8')) # 价格政策
                }

                shopping_car_course_list.append(temp)
            ret['data'] = shopping_car_course_list
        except Exception as e:
            ret['code'] = 10005
            ret['error'] = '获取数据失败'
        return Response(ret)

    def create(self,request,*args,**kwargs):
        # 获取前端传来的课程id 和价格政策
        course_id = request.data.get('course_id')
        policy_id = request.data.get('policyid')
        #2 判断合法性
        # 课程是否存在
        # 价格策略是否合法

        # 2.1 课程是否存在
        course = models.Course.objects.filter(id=course_id).first()
        if not course:
            return Response({'code':10001,'error':'课程不存在'})

        # 2.2 价格策略是否合法
        price_policy_queryset = course.price_policy.all() # 正向操作获取当前对象的所有价格策略对象
        price_policy_dict = {}
        # 循环每一个对象,然后获取相应的值,组成键值对存在在字典中
        for item in price_policy_queryset:
            temp = {
                'id':item.id,
                'price':item.price,
                'valid_period':item.valid_period,
                'valid_period_display':item.get_valid_period_display()
            }
            # 把循环得到的字典,在以用户的id作为键,再放到一个字典中
            price_policy_dict[item.id] =temp

        if policy_id not in price_policy_dict:
            return Response({'code':'10002','error':'课程价格不合法'})
        pattern = settings.LUFFY_SHOPPING_CAR%(USER_ID,'*')

        keys = CONN.keys(pattern)
        print(keys)
        if keys and len(keys) >= 1000:
            return Response({'code':10009,'error':'购物车东西太多,先先去结算之后再添加'})
        key = settings.LUFFY_SHOPPING_CAR%(USER_ID,course_id)
        CONN.hset(key,'id',course_id),
        CONN.hset(key,'name',course.name),
        CONN.hset(key,'img',course.course_img),
        CONN.hset(key,'default_price_id',policy_id),
        CONN.hset(key,'price_policy_dict',json.dumps(price_policy_dict)),
        CONN.expire(key,20*60) # 20分钟过期
        return Response({'code':10000,'data':'购买成功'})

    def destroy(self,request,*args,**kwargs):
        response = BaseResponse()
        try:
            courseid = request.GET.get('courseid')
            key = settings.LUFFY_SHOPPING_CAR % (USER_ID,courseid)
            CONN.delete(key)
            response.data = '删除成功'
        except Exception as e:
            response.code = 10006
            response.error = '删除失败'
            return Response(response.dict)


    def update(self,request,*args,**kwargs):
        response = BaseResponse()
        try:
            course_id = request.data.get('courseid')
            policy_id = str(request.data.get('policyid')) if request.data.get('policyid') else None
            key = settings.LUFFY_SHOPPING_CAR %(USER_ID,course_id)
            if not CONN.exists(key):
                response.code = 10007
                response.error = '课程不存在'
                return Response(response.dict)

            price_policy_dict = json.loads(CONN.hget(key,'price_policy_dict').decode('utf8'))
            if policy_id not in price_policy_dict:
                response.code = 10008
                response.error = '价格策略不存在'
                return Response(response.dict)
            CONN.hset(key,'default_price_id',policy_id)
            CONN.expire(key,20*60)
            response.data = '修改成功'
        except Exception as e:
            response.code = 10009
            response.error = '修改失败'

        return Response(response.dict)

