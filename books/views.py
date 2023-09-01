from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string

from .forms import BookForm, SearchForm
from .models import Book

@login_required(login_url="login")
@permission_required('books.can_view_book_list', raise_exception=True)
def book_list(request):
    try:
        books = Book.objects.active()
        form = SearchForm(request.POST)

        if request.method == 'POST':
            if form.is_valid():
                query = form.cleaned_data['query']
                books = books.filter(Q(publisher__name__icontains=query) | Q(writer__name__icontains=query) |\
                                     Q(writer__surname__icontains=query) | Q(name__icontains=query))

        paginator = Paginator(books, 3)
        page = request.GET.get('page', 1)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        content = {
            'books': books,
            'form': form
        }
        return render(request, "book_list.html", content)
    except Exception as e:
        print('Book List Error!', str(e))
        return redirect('books')


@permission_required('books.can_add_book', raise_exception=True)
def add_book(request):
    try:
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                data = Book()
                data.publisher = form.cleaned_data.get('publisher')
                data.writer = form.cleaned_data.get('writer')
                data.name = form.cleaned_data.get('name')
                data.subject = form.cleaned_data.get('subject')
                data.description = form.cleaned_data.get('description')
                data.isbn = form.cleaned_data.get('isbn')
                data.page_count = int(form.cleaned_data.get('page_count'))
                data.count = int(form.cleaned_data.get('count'))
                data.publisher_date = form.cleaned_data.get('publisher_date')
                data.save()
                messages.success(request, 'Add Successfuly')
                return redirect('books')
            else:
                messages.success(request, 'Book Form Error:' + str(form.errors))
                return redirect('books')
        else:
            form = BookForm()
            context = {'form': form, 'formPage': True}
            html_form = render_to_string('add_book.html',
                                         context,
                                         request=request,
                                         )
            return JsonResponse({'html_form': html_form})
    except Exception as e:
        print("Book add error", str(e))
        return redirect('books')


@permission_required('books.can_edit_book', raise_exception=True)
def edit_book(request, id):
    try:
        book = Book.objects.get(id=id)
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES, instance=book)
            if form.is_valid():
                form.save()
                messages.success(request, 'Book Updated Successfuly')
            else:
                messages.success(request, 'Book Form Error:'+str(form.errors))
            return redirect('books')
        else:
            form = BookForm(instance=book)
            context = {'form': form, 'formPage': True}
            html_form = render_to_string('edit_book.html',
                                         context,
                                         request=request,
                                         )
            return JsonResponse({'html_form': html_form})
    except Book.DoesNotExist:
        return redirect('books')


@permission_required('books.can_delete_book', raise_exception=True)
def delete_book(request, id):
    try:
        book = Book.objects.get(id=id)
        book.deactive()
        messages.success(request, 'Book Deleted')
        return redirect('books')
    except Book.DoesNotExist:
        return redirect('books')

