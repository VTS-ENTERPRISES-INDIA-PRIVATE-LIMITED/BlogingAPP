from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Blog, Category, Comment
from .forms import CreateBlogForm, CommentForm
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.http import HttpResponse

def index(request):
    keyword = request.GET.get("search")
    msg = None
    paginator = None

    try:
        template = get_template('BlogApp/index.html')
    except TemplateDoesNotExist:
        return HttpResponse("Template not found.")
    
    if keyword:
        blogs = Blog.objects.filter(
            Q(title__icontains=keyword) | 
            Q(body__icontains=keyword) | 
            Q(category__title__icontains=keyword)
        ).distinct().select_related('category').prefetch_related('comments')
        
        if blogs.exists():
            paginator = Paginator(blogs, 4)
            blogs = paginator.page(1)
        else:
            msg = "There is no article with the keyword"
    else:
        blogs = Blog.objects.filter(featured=False).select_related('category').prefetch_related('comments')
        paginator = Paginator(blogs, 4)
        page = request.GET.get("page")
        
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    context = {
        "blogs": blogs, 
        "msg": msg, 
        "paginator": paginator, 
        "cats": categories, 
        'is_index_page': True,  
        'show_footer': True,
    }
    return render(request, "BlogApp/index.html", context)



def detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    related_blogs = Blog.objects.filter(category__id=blog.category.id).exclude(id=blog.id)[:4]
    comments = Comment.objects.filter(blog=blog)
    form = CommentForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user 
                comment.save()
                return redirect("detail", slug=blog.slug)
    context = {'blog': blog, "form": form, "comments": comments, "r_blogs": related_blogs, 'is_index_page': False,  'show_footer': True,}
    return render(request, "BlogApp/detail.html", context)


@login_required(login_url="signin")
def create_article(request):
    if request.user.is_authenticated:
        user =request.user
        form =CreateBlogForm()
        if request.method =='POST':
            form = CreateBlogForm(request.POST, request.FILES)
            if form.is_valid():
                Blog = form.save(commit=False)
                Blog.slug =slugify(request.POST["title"])
                Blog.user = request.user
                Blog.save()
                messages.success(request,"Article created successfully!")
                
                return redirect('profile')

    context={'form':form, 'is_index_page': False,  'show_footer': True,}
    return render(request, "BlogApp/create.html", context)

@login_required(login_url="signin")
def update_article(request, slug):
    update = True
    blog = Blog.objects.get(slug=slug)
    form=CreateBlogForm(instance=blog)
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES, instance=blog)
        blog = form.save(commit=False)
        blog.slug=slugify(request.POST["title"])
        blog.save()
        messages.success(request, "Article updated successfully")
        return redirect("profile")
    context={"update":update, "form":form, 'is_index_page': False,  'show_footer': True,}
    return render(request, "BlogApp/create.html", context)


@login_required(login_url="signin")
def delete_article(request, slug):
    blog = Blog.objects.get(slug=slug)
    blogs = Blog.objects.filter(user=request.user)
    delete_article = True
    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Article deleted successfully")
        return redirect("profile")
    context = {"blog": blog, "del":delete_article, "blogs": blogs, 'is_index_page': False,  'show_footer': True,}
    return render(request, "core/profile.html", context)
    


    