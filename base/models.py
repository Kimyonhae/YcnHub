from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AbstractUser
import os;


# 외부 경로 정의
EXTERNAL_ROOT = os.path.join(os.path.expanduser("~"), "Desktop", "저장공간")
# 외부 저장소 생성
external_storage = FileSystemStorage(location=EXTERNAL_ROOT)


class CustomUser(AbstractUser):
    # 사용자 모델에 닉네임 필드 추가
    nickname = models.CharField(max_length=8, blank=False)
    storage = models.BigIntegerField(default=2147483648)  # 수정 불가능한 필드


class Folder(models.Model):
    # 폴더 모델 정의, 각 폴더는 하나의 사용자에 속함
    title = models.CharField(max_length=20, blank=False, null=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # 사용자가 삭제되면 해당 사용자의 폴더도 삭제
        related_name="folders",  # 사용자 입장에서 폴더를 조회할 때 사용할 이름
    )


def fildPathDefine(instance, filename):
    # 현재 사용자 홈 디렉토리 기반으로 경로 생성
    return os.path.join("저장공간",instance.folder.user.username ,instance.folder.title, filename)


#"../../../{instance.folder.user.username}/Desktop/저장공간/{instance.folder.title}/{filename}"

class UploadedFile(models.Model):
    extends_path = os.path.join("home", )
    # 파일 모델 정의, 각 파일은 하나의 폴더에 속함
    file = models.FileField(upload_to=fildPathDefine)
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,  # 폴더가 삭제되면 해당 폴더의 파일도 삭제
        related_name="files",  # 폴더 입장에서 파일을 조회할 때 사용할 이름
    )
