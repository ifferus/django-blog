from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View 

from .models import *
from .utils import *
from .forms import TagForm, PostForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.db.models import Q

#Вывод постов
def post_list(request):
#Поисковик
	query_search = request.GET.get('search', '')

	if query_search:
		posts = Post.objects.filter(Q(title__icontains=query_search) | Q(body__icontains=query_search))
	else:
		posts = Post.objects.all()

	paginator = Paginator(posts, 2)

#Пагинация
	page_number_web = request.GET.get('page', 1)
	page = paginator.get_page(page_number_web)

	is_paginatated = page.has_other_pages()


	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''

	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''
	
	context = {
		'page_object': page,
		'is_paginatated': is_paginatated,
		'next_url': next_url,
		'prev_url':prev_url,
		'query_search': query_search,
	}

	return render(request, 'blog/index.html', context=context)

#Содержание поста
class PostDetail(ObjectDetailMixin, View):
	model = Post
	template = 'blog/post_detail.html'

#Создание поста
class PostCreate(LoginRequiredMixin,ObjectCreateMixin, View):
	form_model = PostForm
	template = 'blog/post_create_form.html'
	raise_exception = True

#Обновление поста
class PostUpdate(LoginRequiredMixin,ObjectUpdateMixin, View):
	model = Post
	form_model = PostForm
	template = 'blog/post_update_form.html'
	raise_exception = True

#Удаление поста
class PostDelete(LoginRequiredMixin,ObjectDeleteMixin, View):
	model = Post
	template = 'blog/post_delete_form.html'
	redirect_url = "post_list_url"
	raise_exception = True	

#Вывод тэгов
def tags_list(request):
	tags = Tag.objects.all()
	return render(request, 'blog/tags_list.html', context={'tags': tags})

#Создание тэга
class TagCreate(ObjectCreateMixin, View):
	form_model = TagForm
	template = 'blog/tag_create.html'

#Обновление тэга
class TagUpdate(LoginRequiredMixin,ObjectUpdateMixin, View):
	model = Tag
	form_model = TagForm
	template = 'blog/tag_update_form.html'
	raise_exception = True

#Удаление тэга
class TagDelete(LoginRequiredMixin,ObjectDeleteMixin, View):
	model = Tag
	template = 'blog/tag_delete_form.html'
	redirect_url = "tag_list_url"
	raise_exception = True

#Содержание тэга
class TagDetail(LoginRequiredMixin,ObjectDetailMixin, View):
	model = Tag
	template = 'blog/tag_detail.html'
	raise_exception = True
