import shutil
import mimetypes
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import login , logout
from django.http import FileResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.core.exceptions import SuspiciousFileOperation

from .models import Folder, UploadedFile
from .forms import RegisterForm, LoginForm, FolderWithUserForm, FileUploadForm
import os, json

# Create your views here.

class Main(View):
    def get(self, req):
        if req.user.is_authenticated:
            folderPath = f"저장공간/{req.user}"
            folderList = os.listdir(folderPath)

            return render(
                req,
                "base/base.html",
                context={"user": req.user, "folderList": folderList},
            )
        else:
            return redirect("login")

    def post(self, req):
        if req.user.is_authenticated:
            folderCreatePath = f"저장공간/{req.user}/{req.POST['title']}"

            #폴더 만들기
            os.makedirs(folderCreatePath, exist_ok=True) 

            return redirect('index')
            
        else:
            return redirect("login")

class FolderView(View):
    def get(self,req, folderName):
        folderPath = f"저장공간/{req.user}"
        folderList = os.listdir(folderPath)
        
        # folder 내부의 파일들을 read
        folderPath += f"/{folderName}"
        # 폴더 내부 파일 read

        
        try:
            files = os.listdir(folderPath)

            return render(
            req,
            'base/base.html', 
            context={
                "folderList" :folderList,
                "folderName" : folderName,
                "files" :files,
            }
        )
        except:
            return render(
                req,
                "base/base.html",
                context={"user": req.user, "folderList": folderList},
            )        

    def post(self ,req, folderName):
        folderPath = f"저장공간/{req.user}"

        folderPath += f"/{folderName}"

        fileObj = req.FILES['file']

        fs = FileSystemStorage(location=folderPath)
        fs.save(fileObj.name, fileObj)

        return redirect('folder_page', folderName=folderName)
    
    def patch(self,req, folderName):
        try:
            nextFolderName = json.loads(req.body)  
            currentFolderPath = os.path.join("저장공간", str(req.user), folderName)
            nextFolderPath = os.path.join("저장공간", str(req.user), nextFolderName['title'])

            os.rename(currentFolderPath, nextFolderPath)
          
            folderPath = f"저장공간/{req.user}"

            return JsonResponse({'status' : "success"})
        except:
            return custom_404_fn("수정에 문제가 생겼습니다")
        
    def delete(self,req, folderName):
        try:
            deletePath = os.path.join("저장공간", str(req.user), folderName)
            shutil.rmtree(deletePath)
            return JsonResponse({'status' : "success"})
        except:
            return custom_404_fn("문제가 생겼습니다")


class FileView(View):
    def get(self, req, folderName, fileName):
        folderPath = f"저장공간/{req.user}"
        folderList = os.listdir(folderPath)        
        
        files = os.listdir(f"저장공간/{req.user}/{folderName}")

        return render(req, 'base/base.html',           
            context={
                "folderList" :folderList,
                "folderName" : folderName,
                "files" :files,
                "selectedFile" :fileName,
            },
        )
    
    def post(self, req, folderName, fileName):
        download_path = os.path.join("저장공간",str(req.user) ,folderName, fileName)
        try:
            if os.path.exists(download_path):
                return FileResponse(open(download_path, 'rb'), as_attachment=True)
            else:
                return custom_404_fn(req,"파일을 찾을 수 없습니다")
        except:
            return custom_404_fn(req,"파일을 찾을 수 없습니다")
        

    def delete(self, req, folderName, fileName):
        file_path = f"저장공간/{req.user}/{folderName}/{fileName}"
        try:
            if os.path.exists(file_path):
                os.remove(file_path)  # 하드 디스크 파일 삭제
                return JsonResponse({'success' : 'True'})
            else:
                return custom_404_fn(req, "파일을 삭제 할 수 없습니다.")
        except Exception as e:
            return custom_404_fn(req, "파일 삭제 오류입니다.")

class LoginView(View):
    def get(self, req):
        if req.user.is_authenticated:
            return redirect('index')
        else:
            return render(req, "base/login.html")

    def post(self, req):
        loginForm = LoginForm(req.POST)
        if loginForm.is_valid():
            login(req, loginForm.cleaned_data.get("user"))            
            return redirect("index")
        else:
            return render(req, "base/login.html", {"form": loginForm})


class LogoutView(View):
    def get(self, req):
        logout(req)
        return redirect("login")



def custom_404_fn(req, message="접근 권한이 업습니다"):
    return render(req, '404.html', status=404,context={'message' : message})

# class Register(View):

#     def post(self, req):
#         print(req.POST)
#         form = RegisterForm(req.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("login")
#         return render(req, "base/register.html", {"form": form})

#     def get(self, req):
#         form = RegisterForm()
#         return render(req, "base/register.html", {"form": form})


# 계정을 잃어버린 경우
# def forgotPassword(req):
#     return render(req, "base/forgot_password.html")
