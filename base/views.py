import shutil
import mimetypes
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import login, logout
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


from .models import Folder, UploadedFile
from .forms import RegisterForm, LoginForm, FolderWithUserForm, FileUploadForm, SizeRestrictForm
import os, json


# Create your views here.


class Main(View):
    def get(self, req):
        if req.user.is_authenticated:
            folderlist = Folder.objects.all()
            
            print(f"User Storage : {req.user.storage}")
            return render(
                req,
                "base/base.html",
                context={"user": req.user, "folderList": folderlist},
            )
        else:
            return redirect("login")

    def post(self, req):
        # folder title 가져오고 user 가 있는지 확인 이제 folder를 만듬과 동시에 Ubuntu 서버 하드디스크에 folderModel의 title을 가지는 Folder를 만들어야함.
        if req.user.is_authenticated:
            folderForm = FolderWithUserForm(req.POST)
            folderlist = Folder.objects.all()
            if folderForm.is_valid():
                folderForm.save()  # 저장

                # 실제 폴더를 만들어야함. test를 위해 현재 프로젝트 내부에 Test
                os.makedirs(
                    os.path.join(
                        "location",
                        str(folderForm.cleaned_data["user"]),
                        folderForm.cleaned_data["title"],
                    ),
                    exist_ok=True,
                )

                return redirect("index")
            return render(
                req,
                "base/base.html",
                context={"user": req.user, "folderList": folderlist},
            )
        else:
            return redirect("login")


class FileView(View):

    def get(self, req, folderId, fileId):
        print(f"folderId={folderId} / fileId={fileId}")
        folderlist = Folder.objects.filter(user_id=req.user.id)
        print("folderlist : ", folderlist)
        files = UploadedFile.objects.filter(folder_id=folderId)
        file_data = [
            {
                "id": file.id,
                "name": file.file.name.split("/")[-1],
                "url": file.file.path,
            }
            for file in files
        ]

        total_volume = sum(file.file.size for file in files)
        savedVolume = SizeRestrictForm.helpByteCalcurator(total_volume)
        if fileId:
            selectedFile = get_object_or_404(UploadedFile, id=fileId)
            selectedFile = {
                "id": selectedFile.id,
                "name": selectedFile.file.name.split("/")[-1],
                "url": selectedFile.file.path,
            }
            return render(
                req,
                "base/base.html",
                context={
                    "user": req.user,
                    "folderList": folderlist,
                    "selectedFolder": folderId,
                    "selectedFile": selectedFile,
                    "files": file_data,
                    "usingVol": savedVolume,
                },
            )
        else:
            return redirect("folder_view")

    def post(self, req, folderId):
        print("Files : ", req.FILES)
        folder = Folder.objects.get(id=folderId)  # 현재 들어와있는 폴더.
        fileForm = FileUploadForm(req.POST, req.FILES)
        if fileForm.is_valid():
            uploaded_file = fileForm.save(commit=False)  # 임시 저장
            uploaded_file.folder = folder
            uploaded_file.save()
            print("파일 생성 됨!!!")
        else:
            print(fileForm.errors)
        return redirect("folder_view", folderId=folderId)

class FileBox(View):

    def get(self, req, folderId, fileId):
        file = get_object_or_404(UploadedFile, id=fileId, folder_id=folderId)
        file_name = file.file.name.split("/")[-1]  # 파이르이 제목
        file_path = file.file.path.replace(file_name, "")  # 제목을 없애고 폴더 까지만.
        print(f"filePath : {file_path}, fileName : {file_name}")
        fs = FileSystemStorage(file_path)
        # 파일 확장자에 따른 타입 결정.
        mime_type, encoding = mimetypes.guess_type(file_name)
        print(f"mime_type : {mime_type}, encoding : {encoding}")

        if mime_type is None:
            mime_type = "application/octet-stream"

        response = FileResponse(fs.open(file_name, "rb"), content_type=mime_type)
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'

        return response

    def delete(self, req, folderId, fileId):
        try:
            folder = Folder.objects.get(id=folderId)
            file = get_object_or_404(UploadedFile, id=fileId, folder_id=folderId)
            file.delete()
            filename = file.file.name.split("/")[-1]
            os.remove(
                os.path.join("location", str(folder.user), folder.title, filename)
            )
            return JsonResponse({"success": True}, status=200)
        except OSError as e:
            print(f"파일 삭제에 실패했습니다 : {e}")
            return JsonResponse({"success": False}, status=400)
        except:
            print("파일 삭제에 문제가 생겼습니다.")
            return JsonResponse({"success": False}, status=400)


class FolderView(View):
    def get(self, req, folderId):
        if req.user.is_authenticated:
            folderlist = Folder.objects.all()
            
            
            files = UploadedFile.objects.filter(folder_id=folderId)
            print(f"folderId : {folderId}")
            
            file_data = [
                {
                    "id": file.id,
                    "name": file.file.name.split("/")[-1],
                    "url": file.file.path,
                }
                for file in files
            ]
            
            print(f"folder title : {[folder.title for folder in folderlist]}")
            
            total_volume = sum(file.file.size for file in files)

            savedVolume = SizeRestrictForm.helpByteCalcurator(total_volume)
            
            if len(files) > 0:
                folder = Folder.objects.get(id=folderId)
                filename = [file.file.name for file in files][-1]
                store_is_vaild = SizeRestrictForm.storageOfSize_is_vaild(req.user.storage , savedVolume)
                print(f"savedVolume : {savedVolume}")
                if store_is_vaild == False: # 누적된 파일이 용향을 오버했을 때
                    # 마지막 저장한 파일을 지우는 로직
                    lastFile_id = files.last().id
                    
                    # db에서 UploadedFile제거
                    UploadedFile.objects.get(id=lastFile_id).delete()
                    # 하드웨어에서도 제거해야함.
                    os.remove(
                        os.path.join("location", str(folder.user), folder.title, filename)
                    )
                    
                    messages.warning(req, "용량 초과입니다. 문의하세요")
                    return redirect('folder_view', folderId=folderId)  # 리디렉트로 페이지 새로고침
            return render(
            req,
            "base/base.html",
            context={
                "user": req.user,
                "folderList": folderlist,
                "selectedFolder": folderId,
                "files": file_data,
                "usingVol": savedVolume,
            },
            )
        else:
            return redirect("login")

    def patch(self, req, folderId):
        if req.user.is_authenticated:
            folder = Folder.objects.get(id=folderId)
            prevFolderTitle = folder.title
            data = json.loads(req.body)  # data Parsing
            try:
                if data and "title" in data:
                    folder.title = data["title"]
                    folder.save()
                    response_data = {
                        "status": "success",
                        "message": "업데이트 성공",
                        "folder": {
                            "id": folder.id,
                            "title": folder.title,
                        },
                    }

                    # 바뀐 폴더에 따라 file의 path를 바꿔준다.
                    files = UploadedFile.objects.filter(folder_id=folderId)
                    if files.filter(folder_id=folderId):
                        for file in files:
                            filename = file.file.name.split("/")[-1]
                            file.file.name = f"location/{folder.user.username}/{folder.title}/{filename}"
                            file.save()
                    # 파일 이름 바꾸는 기능.
                    os.rename(
                        os.path.join("location", str(folder.user), prevFolderTitle),
                        os.path.join("location", str(folder.user), folder.title),
                    )
            except json.JSONDecodeError:
                return JsonResponse(
                    {"status": "fail", "message": "유효하지 않은 값입니다."}, status=400
                )
            except Folder.DoesNotExist:
                return JsonResponse(
                    {"status": "fail", "message": "폴더를 찾을 수 없습니다."},
                    status=404,
                )
            return JsonResponse(data=response_data, status=200)
        else:
            return JsonResponse(
                {"status": "fail", "message": "허용된 접근이 아닙니다."}, status=404
            )

    def delete(self, req, folderId):
        if req.user.is_authenticated:
            print("delete 삭제 들어옴", folderId)
            folder = Folder.objects.get(id=folderId)
            folder.delete()
            response_data = {
                "status": "success",
                "message": "업데이트 성공",
                "folder": {
                    "id": folder.id,
                    "title": folder.title,
                },
            }
            try:
                # 하드 디스크에 Folder 삭제 and 권한 설정 pass.
                shutil.rmtree(os.path.join("location", str(folder.user), folder.title))
            except OSError as e:
                print(f"파일 삭제에 실패했습니다 : {e}")

            return JsonResponse(data=response_data, status=200)
        else:
            return redirect("login")


class LoginView(View):
    def get(self, req):
        if req.user.is_authenticated:
            return redirect('index')
        else:
            return render(req, "base/login.html")

    def post(self, req):
        loginForm = LoginForm(req.POST)
        if loginForm.is_valid():
            login(req, loginForm.cleaned_data["user"])

            return redirect("index")
        else:
            return render(req, "base/login.html", {"form": loginForm})


class LogoutView(View):
    def get(self, req):
        logout(req)
        return redirect("login")


class Register(View):

    def post(self, req):
        print(req.POST)
        form = RegisterForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(req, "base/register.html", {"form": form})

    def get(self, req):
        form = RegisterForm()
        return render(req, "base/register.html", {"form": form})


# 계정을 잃어버린 경우
def forgotPassword(req):
    return render(req, "base/forgot_password.html")
