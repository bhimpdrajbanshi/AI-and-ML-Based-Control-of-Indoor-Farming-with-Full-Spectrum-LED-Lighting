from django.shortcuts import render, get_object_or_404, redirect
from ..models import Vegetable
from django.contrib.auth.decorators import login_required

# List all vegetables
def vegetable_list(request):
    vegetables = Vegetable.objects.all()
    return render(request, 'admin/vegetables/vegetable_list.html', {'vegetables': vegetables})

# Create a new vegetable
# @login_required
def vegetable_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_available = 'is_available' in request.POST  # checkbox returns only if checked
        image = request.FILES.get('image')

        # Save to DB
        Vegetable.objects.create(
            name=name,
            description=description,
            is_available=is_available,
            image=image
        )

        return redirect('vegetable_list')  # Adjust as needed

    return render(request, 'admin/vegetables/add_vegetable.html')
# Edit an existing vegetable
@login_required
def vegetable_edit(request, pk):
    vegetable = get_object_or_404(Vegetable, pk=pk)
    form = VegetableForm(request.POST or None, request.FILES or None, instance=vegetable)
    if form.is_valid():
        form.save()
        return redirect('vegetable_list')
    return render(request, 'vegetables/vegetable_form.html', {'form': form})

# Delete a vegetable
@login_required
def vegetable_delete(request, pk):
    vegetable = get_object_or_404(Vegetable, pk=pk)
    if request.method == 'POST':
        vegetable.delete()
        return redirect('vegetable_list')
    return render(request, 'vegetables/vegetable_confirm_delete.html', {'vegetable': vegetable})
