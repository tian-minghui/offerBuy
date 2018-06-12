from django.db import models


# Create your models here.
class BaseModel(models.Model):
    user_id = models.CharField(max_length=50)
    create_date = models.DateField(auto_now_add=True)


class User(BaseModel):
    """
    用户模型
    """
    user_id = models.CharField(max_length=50, unique=True)
    is_valid = models.BooleanField(default=False)  # 是否已经取消关注
    pass


class Rebate(BaseModel):
    """
    返利表
    """
    source_url = models.TextField(null=False)
    pass
