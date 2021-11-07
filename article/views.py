from typing import Reversible
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse,reverse

from .forms import ArticleForm
from django.contrib import messages
from .models import Article,Comment
from django.contrib.auth.decorators import login_required



def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})
    
    articles = Article.objects.all() # if the keyword is not typed we can show all of the Articles

    return render(request,"articles.html",{"articles":articles})




def index(request):
    context = {
        # "number1":10,
        # "number2":20
        "numbers":[1,2,3,4,5,6]

    }
    return render(request,"index.html",context)


def about(request):
    return render(request,"about.html")



def detail(request,id):
    # article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article,id = id)
    comments = article.comments.all()

    return render(request,"detail.html",{"article":article,"comments":comments}) # Detail:20 Detail:30 


@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }
    return  render(request,"dashboard.html",context)



def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article =  form.save(commit = False) # commit = false ile sen şu an kaydetme ben sonra kaydedicem diyorsun
        article.author = request.user # request'ten gelen user bilgisi
        article.save()
        
        messages.success(request,"Makale başarıyla oluşturuldu")
        return redirect("article:dashboard")
        

    return render(request,"addarticle.html",{"form":form})

def updateArticle(request,id):

    article = get_object_or_404(Article,id=id)
    form = ArticleForm(request.POST or None, request.FILES or None,instance = article) 
    # instance = article -- create a new article instance  
    
    if form.is_valid():
        article =  form.save(commit = False) 
        article.author = request.user 
        article.save()

        messages.success(request,"Makale başarıyla güncellendi")
        return redirect("article:dashboard")

    
    return render(request,"update.html",{"form":form})

def deleteArticle(request,id):

    article = get_object_or_404(Article,id = id)
    article.delete()
    messages.success(request,"Makale başarıyla silindi")

    return redirect("article:dashboard")


def addComment(request,id):
    article = get_object_or_404(Article,id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)

        newComment.article = article 
        newComment.save()

    return redirect(reverse("article:detail",kwargs={"id":id})) # both get and post request