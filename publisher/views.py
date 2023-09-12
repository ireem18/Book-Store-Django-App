from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import permission_required, login_required

from base.generators import paginator
from .forms import PublisherForm
from .models import Publisher


@login_required(login_url="login")
@permission_required('publisher.view_publisher', raise_exception=True)
def publisher_list(request):
    form = PublisherForm()
    page = request.GET.get('page', 1)
    publishers = paginator(page, Publisher)

    content = {
        'publishers': publishers,
        'form': form
    }
    return render(request, "publisher_list.html", content)


@login_required(login_url="login")
@permission_required('publisher.add_publisher', raise_exception=True)
def add_publisher(request):
    try:
        page = request.GET.get('page', 1)
        publishers = paginator(page, Publisher)
        if request.method == 'POST':
            form = PublisherForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Add Successfuly')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return render(request, 'publisher_list.html', {'form': form, 'publishers': publishers})
        else:
            form = PublisherForm()
        return render(request, 'publisher_list.html', {'form': form})

    except Exception as e:
        print("Publisher add error", str(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="login")
@permission_required('publisher.change_publisher', raise_exception=True)
def edit_publisher(request, id):
    try:
        publisher = Publisher.objects.get(id=id)
        print(request.method)
        page = request.GET.get('page', 1)
        publishers = paginator(page, Publisher)

        if request.method == 'POST':
            form = PublisherForm(request.POST, request.FILES, instance=publisher)
            if form.is_valid():
                form.save()
                messages.success(request, 'Publisher Updated Successfuly')
                return redirect('publishers')
            else:
                return render(request, 'publisher_list.html', {'form': form, 'publishers': publishers})

        else:
            form = PublisherForm(instance=publisher)
            print("form")
            return render(request, 'publisher_list.html', {'form': form, 'publishers': publishers})

    except Publisher.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="login")
@permission_required('publisher.delete_publisher', raise_exception=True)
def delete_publisher(request, id):
    try:
        publisher = Publisher.objects.get(id=id)
        publisher.deactive(publisher)
        messages.success(request, 'Publisher Deleted')
    except Exception as e:
        messages.error(request, 'Publisher Not Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
