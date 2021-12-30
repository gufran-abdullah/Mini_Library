from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	enrollment = models.CharField(max_length=50)
	branch = models.CharField(max_length=20)

	def __str__(self):
		return self.user.username


class BookCategorie(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Book(models.Model):
	bookname = models.CharField(max_length=150)
	authorname = models.CharField(max_length=200)
	category = models.ForeignKey(BookCategorie,on_delete=models.CASCADE)
	isbnno = models.CharField(max_length=50)
	quantity = models.IntegerField(default=0)

	def __str__(self):
		return self.bookname +' '+'['+ self.category.name +']'


class IssueBook(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	book = models.ForeignKey(Book,on_delete=models.CASCADE)
	issue_date = models.DateField()
	due_date = models.DateField()

	def __str__(self):
		return self.student.user.username+' ['+self.book.bookname+'] ' 