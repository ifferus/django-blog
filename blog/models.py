from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify
from time import time 


def gen_slug(s):#Генерация слага для апдейта постов и тэгов
	new_slug = slugify(s, allow_unicode=True)
	return new_slug + '-' + str(int(time()))


# Create your models her.
class Post(models.Model):
	title = models.CharField(max_length=150, db_index=True)
	slug = models.SlugField(max_length=150, blank=True, unique=True)
	body = models.TextField(blank=True, db_index=True)
	tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
	date_pub = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):# название из соглашение django
		return reverse('post_detail_url', kwargs={'slug': self.slug })
		"""Возращает ссылку на конкретный объект.
		   Именно объекта из класса Post.
		"""
	def get_update_url(self):
		return reverse('post_update_url', kwargs={'slug': self.slug})

	def get_delete_url(self):
		return reverse('post_delete_url', kwargs={'slug': self.slug})



	def save(self, *args, **kwargs):
		if not self.id:#Проверка на сохранение через if
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-date_pub']
		
			

class Tag(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True)

	def get_absolute_url(self):
		return reverse('tag_detail_url', kwargs={'slug': self.slug})

	def get_update_url(self):
		return reverse('tag_update_url', kwargs={'slug': self.slug})

	def get_delete_url(self):
		return reverse('tag_delete_url', kwargs={'slug': self.slug})


	def __str__(self):
		return '{}'.format(self.title)

	class Meta:
		ordering = ['-title']