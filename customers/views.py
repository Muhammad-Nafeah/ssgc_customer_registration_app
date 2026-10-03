from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomerRegistration
from .forms import CustomerForm
from django.db.models import Q
from django.contrib import messages #pop us message
from django.core.paginator import Paginator 
from django.contrib.auth.decorators import login_required


@login_required
def customer_list(request):
    q = request.GET.get('q', '').strip()
    customers = CustomerRegistration.objects.all().order_by('UR_CONSUMER_S_NO')

    if q:
        customers = customers.filter(
            Q(FULL_NAME__icontains=q) |
            Q(CNIC__icontains=q) |
            Q(CLAIM_ID__icontains=q)
        )

    total = customers.count()
    paginator = Paginator(customers, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'customers/customer_list.html', {
        'page_obj': page_obj,
        'q': q,
        'total': total,
    })
@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(CustomerRegistration, pk=pk)

    sections = []
    for title, icon, names in CustomerForm.SECTIONS:
        rows = []
        for name in names:
            label = CustomerRegistration._meta.get_field(name).verbose_name
            rows.append((label, getattr(customer, name)))
        sections.append({'title': title, 'icon': icon, 'rows': rows})

    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'sections': sections,
    })
@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Add Customer'})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(CustomerRegistration, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Edit Customer'})

def renumber_customers():
    with connection.cursor() as cursor:
        cursor.execute("SET @n = 0")
        cursor.execute(
            "UPDATE customer_registration "
            "SET UR_CONSUMER_S_NO = (@n := @n + 1) "
            "ORDER BY UR_CONSUMER_S_NO"
        )
        cursor.execute("ALTER TABLE customer_registration AUTO_INCREMENT = 1")

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(CustomerRegistration, pk=pk)
    if request.method == 'POST':
        customer.delete()
        renumber_customers()                                  # <- the new line
        messages.success(request, 'Customer deleted.')
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})





