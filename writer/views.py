from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required

from base.generators import paginator
from .forms import WriterForm
from .models import Writer


@login_required(login_url="login")
@permission_required('writer.can_view_writer_list', raise_exception=True)
def writer_list(request):
    form = WriterForm()
    page = request.GET.get('page', 1)
    writers = paginator(page, Writer)
    content = {
        'writers': writers,
        'form': form
    }
    return render(request, "writer_list.html", content)


@login_required(login_url="login")
@permission_required('writer.can_add_writer', raise_exception=True)
def add_writer(request):
    try:
        page = request.GET.get('page', 1)
        writers = paginator(page, Writer)
        if request.method == 'POST':
            form = WriterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Add Successfuly')
                return redirect('writers')
            else:
                return render(request, 'writer_list.html', {'form': form, 'writers': writers })
        else:
            form = WriterForm()
            context = {
                'form': form
            }
        return render(request, 'writer_list.html', context)

    except Exception as e:
        print("Writer add error", str(e))
        return redirect('writers')


@login_required(login_url="login")
@permission_required('writer.can_edit_writer', raise_exception=True)
def edit_writer(request, id):
    try:
        writer = Writer.objects.get(id=id)
        page = request.GET.get('page', 1)
        writers = paginator(page, Writer)

        if request.method == 'POST':
            form = WriterForm(request.POST, request.FILES, instance=writer)
            if form.is_valid():
                form.save()
                messages.success(request, 'Writer Updated Successfuly')
                return redirect('writers')
            else:
                return render(request, 'writer_list.html', {'form': form, 'writers': writers })
        else:
            form = WriterForm(instance=writer)
            context = {
                'form': form,
                'writers': writers
            }
            return render(request, 'writer_list.html', context)

    except Writer.DoesNotExist:
        return redirect('writers')


@login_required(login_url="login")
@permission_required('writer.can_delete_writer', raise_exception=True)
def delete_writer(request, id):
    try:
        writer = Writer.objects.get(id=id)
        writer.deactive(writer)
        messages.success(request, 'Writer Deleted')
    except Exception as e:
        messages.warning(request, 'Writer Not Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def publisher_of_writers(request):
    publisher = request.GET.get('publisher_id')
    writers = writerList = []
    if publisher:
        writers = Writer.objects.active().filter(publisher_id=publisher)
    for w in writers:
        writerList.append({'id': w.id, 'name': w.__str__()})

    return JsonResponse(writerList, safe=False)
