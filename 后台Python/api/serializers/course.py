
from rest_framework import serializers
from api import models

class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CourseModelSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display') # 自己的字段
    hours = serializers.CharField(source='coursedetail.hours') # 一对一,反向
    course_slogan = serializers.CharField(source='coursedetail.course_slogan') # 一对一,反向
    # coursechaptername = serializers.CharField(source='coursechapter.name') # 一对多 反向
    # recommend_courses = serializers.CharField(source='coursedetail.recommend_courses.all') # 多对多

    recommend_courses = serializers.SerializerMethodField()
    # summary = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['id','name','level_name','hours','course_slogan','recommend_courses','summary']

    def get_recommend_courses(self,row): # 多对多
        recommend_list = row.coursedetail.recommend_courses.all()
        print(888)
        return [ {'id':item.id,'name':item.name} for item in recommend_list]

    def get_summary(self,row):
        summary_list = row.coursechapter.all()
        print(777,summary_list)
        return [item for item in summary_list]