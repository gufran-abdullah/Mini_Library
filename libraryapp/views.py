from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import datetime


def index(request):

	return render(request,'index.html')

def student_login(request):  
	if request.method == 'POST':
		un = request.POST['uname']
		psd = request.POST['pwd']
 
		user = authenticate(username=un,password=psd)

		if user is not None:
			login(request,user)
			messages.success(request,'Student Logged In Successfully.')
			return redirect('student_home')
		else:
			messages.error(request,'Invalid Student Credentials. Try Again!')
			return redirect('student_login')	

	return render(request,'student_login.html')

def student_signup(request):
	if request.method == 'POST':
		fn = request.POST['fname']
		ln = request.POST['lname']
		un = request.POST['uname']
		psd = request.POST['pwd']
		enn = request.POST['enrlno']
		br = request.POST['branch']

		try:
			user = User.objects.create_user(first_name=fn,last_name=ln,username=un,password=psd)
			Student.objects.create(user=user,enrollment=enn,branch=br)
			messages.success(request,'Student Registered Successfully.')
			return redirect('student_login')
		except:
			messages.error(request,'Something Went Wrong.') 
			return redirect('student_signup') 
	return render(request,'student_signup.html')

def student_home(request):
	if not request.user.is_authenticated:
		return redirect('student_login')
	user = request.user
	stdprof = Student.objects.get(user=user) 
	if request.method == 'POST':
		fn = request.POST['fname'] 
		ln = request.POST['lname'] 
		enn = request.POST['enrlno'] 
		br = request.POST['branch']

		stdprof.user.first_name = fn
		stdprof.user.last_name = ln
		stdprof.enrollment = enn
		stdprof.branch = br

		try:
			stdprof.user.save()
			stdprof.save()
			messages.success(request,'Student Profile Updated Successfully.')
			return redirect('student_home')
		except: 
			messages.error(request,'Something Went Wrong.')
			return redirect('student_home')
	context = {
		"stdprof":stdprof
	}
	return render(request,'student_home.html',context)

def student_issuedbooks(request):
	if not request.user.is_authenticated:
		return redirect('student_login')
	user = request.user
	stduser = Student.objects.get(user=user)
	stdissuedbooks = IssueBook.objects.filter(student=stduser)
	context = {
		"stdissuedbooks":stdissuedbooks
	}
	return render(request,'student_issuedbooks.html',context)

def student_issuedbookfine(request,id):
	if not request.user.is_authenticated:
		return redirect('student_login')
	error = False
	issuebook = IssueBook.objects.get(id=id)
	tday = datetime.date.today()
	d1 = issuebook.due_date
	f1 = 0
	d2 = 0
	if tday > d1:
		total_day = tday - d1
		f1 = int(str(total_day)[:-13]) * 10
		d2 = int(str(total_day)[:-13]) 
	else:
		f1 = 0
		d2 = 0
		error = True
	context = {
		"fine":f1,
		"late":d2
	}
	return render(request,'student_issuedbookfine.html',context)

def student_changepassword(request):
	if not request.user.is_authenticated:
		return redirect('student_login')
	if request.method == "POST":
		crntpwd = request.POST['cpwd']
		newpwd = request.POST['npwd']
		cnewpwd = request.POST['cnpwd']
		if newpwd != cnewpwd:
			messages.error(request,"Passwords Doesn't Match.")
			return redirect('student_changepassword')
		else:
			try:
				user = User.objects.get(id=request.user.id)
				if user.check_password(crntpwd):
					user.set_password(newpwd)
					user.save()
					messages.success(request,'Password Changed Successfully.')
					return redirect('student_login')
				else:
					messages.error(request,'Something Went Wrong')
					return redirect('student_changepassword')
			except:
				messages.error(request,'Something Went Wrong')
				return redirect('student_changepassword')
	return render(request,'student_changepassword.html')

def admin_login(request):
	if request.method == 'POST':
		un = request.POST['uname']
		psd = request.POST['pwd']

		user = authenticate(username=un,password=psd)
		try:
			if user.is_staff:
				login(request,user)
				messages.success(request,'Admin Logged In Successfully.')
				return redirect('admin_home')	
			else: 
				messages.error(request,'Invalid Admin Credentials.')
				return redirect('admin_login')
		except:
			messages.error(request,'Invalid Admin Credentials.')
			return redirect('admin_login')
	
	return render(request,'admin_login.html')

def admin_home(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	stds = Student.objects.all().count()
	books = Book.objects.all().count()
	issuedbooks = IssueBook.objects.all().count()
	context = {
		"stds":stds,
		"books":books,
		"issuedbooks":issuedbooks
	}
	return render(request,'admin_home.html',context)

def users_logout(request):
	logout(request)
	messages.success(request,'User Logged out Successfully.')
	return redirect('/')

def admin_registerstudents(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	if request.method == 'POST':
		fn = request.POST['fname']
		ln = request.POST['lname']
		un = request.POST['uname']
		psd = request.POST['pwd']
		enn = request.POST['enrlno']
		br = request.POST['branch']

		try:
			user = User.objects.create_user(first_name=fn,last_name=ln,username=un,password=psd)
			Student.objects.create(user=user,enrollment=enn,branch=br)
			messages.success(request,'Student Registered Successfully.')
			return redirect('admin_managestudents')
		except:
			messages.error(request,'Something Went Wrong.') 
			return redirect('admin_registerstudents') 
	return render(request,'admin_registerstudents.html')

def admin_managestudents(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	all_stds = Student.objects.all().order_by('enrollment')
	context = {
		"all_stds":all_stds
	}
	return render(request,'admin_managestudents.html',context)

def admin_deletestudent(request,id):
	if not request.user.is_staff:
		return redirect('admin_login')
	std = User.objects.get(id=id) 
	std.delete()
	messages.success(request,'Student Deleted Successfully.')
	return redirect('admin_managestudents')

def admin_editstudent(request,id):
	if not request.user.is_staff:
		return redirect('admin_login')
	std = Student.objects.get(id=id)
	if request.method == 'POST':
		fn = request.POST['fname']
		ln = request.POST['lname']
		enn = request.POST['enrlno']
		br = request.POST['branch']

		std.user.first_name = fn
		std.user.last_name = ln
		std.enrollment = enn
		std.branch = br

		try:
			std.user.save()
			std.save()
			messages.success(request,'User Updated Successfully.')
			return redirect('admin_managestudents')
		except:
			messages.success(request,'Something Went Wrong.')
			return redirect('admin_editstudent')
	context = {
		"std":std
	}
	return render(request,'admin_editstudent.html',context)

def admin_addcategory(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	if request.method == 'POST':
		cat = request.POST['categ']

		try: 
			bcat = BookCategorie.objects.create(name=cat)
			bcat.save()
			messages.success(request,'Book Category Added Successfully.')
			return redirect('admin_managecategories')
		except:
			messages.success(request,'Something Went Wrong.')
			return redirect('admin_addcategory')
	return render(request,'admin_addcategory.html')	

def admin_managecategories(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	bookcat = BookCategorie.objects.all().order_by('name')
	context = {
		"bookcat":bookcat
	}
	return render(request,'admin_managecategories.html',context)

def admin_deletecategories(request,id):
	if not request.user.is_staff:
		return redirect('admin_login')
	bcat = BookCategorie.objects.get(id=id)
	bcat.delete()
	messages.success(request,'Book Category Deleted Successfully.')
	return redirect('admin_managecategories')

def admin_editcategory(request,id):
	if not request.user.is_staff:
		return redirect('admin_login')
	bcat = BookCategorie.objects.get(id=id)
	if request.method == 'POST':
		cat = request.POST['categ']

		bcat.name = cat

		try:
			bcat.save()
			messages.success(request,'Book Category Updated Successfully.')
			return redirect('admin_managecategories')
		except:
			messages.success(request,'Something Went Wrong.')
			return redirect('admin_editcategory')
			
	context = {
		"bcat":bcat
	}
	return render(request,'admin_editcategory.html',context)

def admin_addbook(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	bcats = BookCategorie.objects.all().order_by('name')
	if request.method == 'POST':
		bn = request.POST['bname']
		an = request.POST['aname']
		cat = request.POST['categ']
		isbns = request.POST['isbn']
		qtys = request.POST['qty']
		categs = BookCategorie.objects.get(name=cat) 

		try:  
			Book.objects.create(bookname=bn,authorname=an,category=categs,isbnno=isbns,quantity=qtys)
			messages.success(request,'Book Added Successfully.')
			return redirect('admin_managebooks')
		except:
			messages.success(request,'Something Went Wrong.')
			return redirect('admin_addbook')

	context = {
		"bcats":bcats
	} 
	return render(request,'admin_addbook.html',context)

def admin_managebooks(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	books = Book.objects.all().order_by('isbnno')
	context = {
		"books":books
	}
	return render(request,'admin_managebooks.html',context)

def admin_deletebook(request,id): 
	if not request.user.is_staff:
		return redirect('admin_login')
	book = Book.objects.get(id=id)
	book.delete()
	messages.success(request,'Book Deleted Successfully.')
	return redirect('admin_managebooks')

def admin_editbook(request,id):
	if not request.user.is_staff:
		return redirect('admin_login')
	book = Book.objects.get(id=id)
	if request.method == 'POST':
		bn = request.POST['bname']
		an = request.POST['aname']
		isbns = request.POST['isbn']
		qtys = request.POST['qty']
		 
		book.bookname = bn
		book.authorname = an
		book.isbnno = isbns
		book.quantity = qtys
		

		try:                                            
			book.save() 
			messages.success(request,'Book Updated Successfully.')
			return redirect('admin_managebooks')
		except:
			messages.error(request,'Something Went Wrong.')
			return redirect('admin_editbook')
	context = {
		"book":book
	}
	return render(request,'admin_editbook.html',context)

def admin_issuebook(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	stds = Student.objects.all().order_by('enrollment')
	books = Book.objects.all().order_by('isbnno')
	if request.method == 'POST':
		st = request.POST['std']
		bk = request.POST['book']
		isb = request.POST['isbn']

		tday = datetime.date.today()
		tdelta = datetime.timedelta(days=15)
		ex = tday+tdelta

		stu = Student.objects.filter(enrollment=st).first()
		bks = Book.objects.filter(bookname=bk,isbnno=isb).first()
		try:
			if bks.quantity == 0:
				messages.warning(request,'Book is Not Available Right Now.')
				return redirect('admin_issuebook')
			else:
				IssueBook.objects.create(student=stu,book=bks,issue_date=tday,due_date=ex)
				bks.quantity -= 1
				bks.save()
				messages.success(request,'Book Issued Successfully.')
				return redirect('admin_manageissuebook')
		except:
			messages.error(request,'Something Went Wrong.')
			return redirect('admin_issuebook')
	context = {
		"stds":stds,
		"books":books
	}
	return render(request,'admin_issuebook.html',context)

def admin_manageissuebook(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	issuebooks = IssueBook.objects.all()
	context = {
		"issuebooks":issuebooks
	}
	return render(request,'admin_manageissuebook.html',context)

def admin_returnbook(request,id):
	if not request.user.is_staff:
		return redirect('admin_login')
	issuebook = IssueBook.objects.get(id=id)
	b = issuebook.book.id
	retbook = Book.objects.get(id=b)
	issuebook.delete()
	retbook.quantity += 1
	retbook.save()
	messages.success(request,'Book Returned Successfully.')
	return redirect('admin_manageissuebook')

def admin_issuebookfine(request,id):
	if not request.user.is_staff:
		return redirect('admin_login')
	error = False
	issuebook = IssueBook.objects.get(id=id)
	tday = datetime.date.today()
	d1 = issuebook.due_date
	f1 = 0
	d2 = 0
	if tday > d1:
		total_day = tday - d1
		f1 = int(str(total_day)[:-13]) * 10
		d2 = int(str(total_day)[:-13]) 
	else:
		f1 = 0
		d2 = 0
		error = True
	context = {
		"fine":f1,
		"late":d2
	}
	return render(request,'admin_issuebookfine.html',context)

def admin_changepassword(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	if request.method == "POST":
		crntpwd = request.POST['cpwd']
		newpwd = request.POST['npwd']
		cnewpwd = request.POST['cnpwd']
		if newpwd != cnewpwd:
			messages.error(request,"Passwords Doesn't Match.")
			return redirect('admin_changepassword')
		else:
			try:
				user = User.objects.get(id=request.user.id)
				if user.check_password(crntpwd):
					user.set_password(newpwd)
					user.save()
					messages.success(request,'Password Changed Successfully.')
					return redirect('admin_login')
				else:
					messages.error(request,'Something Went Wrong')
					return redirect('admin_changepassword')
			except:
				messages.error(request,'Something Went Wrong')
				return redirect('admin_changepassword')
	return render(request,'admin_changepassword.html')

'''
	

	End Of the project.
	I tried my best to make the project effecient.
	Hence, there are a lot of features would be added to it.

	
'''