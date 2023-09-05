from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required, permission_required

from .forms import WriterForm
from .models import Writer


@login_required(login_url="login")
@permission_required('writer.can_view_writer_list', raise_exception=True)
def writer_list(request):
    writers = Writer.objects.active()
    form = WriterForm()
    paginator = Paginator(writers, 5)
    page = request.GET.get('page', 1)

    try:
        writers = paginator.page(page)
    except PageNotAnInteger:
        writers = paginator.page(1)
    except EmptyPage:
        writers = paginator.page(paginator.num_pages)

    content = {
        'writers': writers,
        'form': form
    }
    return render(request, "writer_list.html", content)


@permission_required('writer.can_add_writer', raise_exception=True)
def add_writer(request):
    try:
        if request.method == 'POST':
            form = WriterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Add Successfuly')
            else:
                messages.warning(request, form.errors)
            return redirect('writers')
        else:
            form = WriterForm()
            context = {
                'form': form
            }
        return render(request, 'writer_list.html', context)

    except Exception as e:
        print("Writer add error", str(e))
        return redirect('writers')


@permission_required('writer.can_edit_writer', raise_exception=True)
def edit_writer(request, id):
    try:
        writer = Writer.objects.get(id=id)
        writers = Writer.objects.active()

        if request.method == 'POST':
            form = WriterForm(request.POST, request.FILES, instance=writer)
            if form.is_valid():
                form.save()
                messages.success(request, 'Writer Updated Successfuly')
            else:
                messages.success(request, 'Writer Form Error:' + str(form.errors))
            return redirect('writers')
        else:
            form = WriterForm(instance=writer)
            context = {
                'form': form,
                'writers': writers
            }
            return render(request, 'writer_list.html', context)

    except Writer.DoesNotExist:
        return redirect('writers')


@permission_required('writer.can_delete_writer', raise_exception=True)
def delete_writer(request, id):
    try:
        writer = Writer.objects.get(id=id)
        writer.deactive('writer')
        messages.success(request, 'Writer Deleted')
    except Exception as e:
        messages.warning(request, 'Writer Not Deleted')
    return redirect('writers')


def publisher_of_writers(request):
    publisher = request.GET.get('publisher_id')
    writers = writerList = []
    if publisher:
        writers = Writer.objects.active().filter(publisher_id=publisher)
    for w in writers:
        writerList.append({'id': w.id, 'name': w.__str__()})

    return JsonResponse(writerList, safe=False)
