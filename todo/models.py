from django.db import models
from users.models import User
from django.utils import timezone
import datetime


class Todo(models.Model):
    user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=50)
    is_complete = models.BooleanField('완료여부', default=False)
    created_at = models.DateTimeField('생성시간', auto_now_add=True)
    updated_at = models.DateTimeField('수정시간', auto_now=True)
    completion_at = models.DateTimeField('완료시간', null=True, blank=True) # is_complete가 True가 된 시각을 기록하도록 할 수 있을까?

    def __str__(self):
        return str(self.title)

    def complete_check(self):
        '''is_complete가 True가 될 때 completion_at의 시간을 기록하고 싶은 함수'''
        if self.is_complete == True:
            self.completion_at = timezone.now() # https://velog.io/@inyong_pang/Django-RuntimeWarning-DateTimeField-received-a-naive-datetime
        return self.completion_at
