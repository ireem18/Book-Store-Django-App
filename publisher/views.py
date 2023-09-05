from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import permission_required, login_required

from .forms import PublisherForm
from .models import Publisher

@login_required(login_url="login")
@permission_required('publisher.view_publisher', raise_exception=True)
def publisher_list(request):
    publishers = Publisher.objects.active()
    form = PublisherForm()
    paginator = Paginator(publishers, 5)
    page = request.GET.get('page', 1)

    try:
        publishers = paginator.page(page)
    except PageNotAnInteger:
        publishers = paginator.page(1)
    except EmptyPage:
        publishers = paginator.page(paginator.num_pages)

    content = {
        'publishers': publishers,
        'form': form
    }
    return render(request, "publisher_list.html", content)


@permission_required('publisher.add_publisher', raise_exception=True)
def add_publisher(request):
    try:
        if request.method == 'POST':
            form = PublisherForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Add Successfuly')
            else:
                messages.success(request, 'Publisher Form Error:' + str(form.errors))
            return redirect('publishers')
        else:
            form = PublisherForm()
            context = {
                'form': form
            }
        return render(request, 'publisher_list.html', context)
    except Exception as e:
        print("Publisher add error", str(e))
        return redirect('publishers')


@permission_required('publisher.change_publisher', raise_exception=True)
def edit_publisher(request, id):
    try:
        publisher = Publisher.objects.get(id=id)
        publishers = Publisher.objects.active()

        if request.method == 'POST':
            form = PublisherForm(request.POST, request.FILES, instance=publisher)
            if form.is_valid():
                form.save()
                messages.success(request, 'Publisher Updated Successfuly')
            else:
                messages.success(request, 'Publisher Form Error:' + str(form.errors))
            return redirect('publishers')
        else:
            form = PublisherForm(instance=publisher)
            context = {
                'form': form,
                'publishers': publishers
            }
            return render(request, 'publisher_list.html', context)

    except Publisher.DoesNotExist:
        return redirect('publishers')


@permission_required('publisher.delete_publisher', raise_exception=True)
def delete_publisher(request, id):
    try:
        publisher = Publisher.objects.get(id=id)
        publisher.deactive('publisher')
        messages.success(request, 'Publisher Deleted')
    except Exception as e:
        messages.error(request, 'Publisher Not Deleted')
    return redirect('publishers')
