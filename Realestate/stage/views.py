from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Property, Transaction
from django.contrib.auth.forms import AuthenticationForm
from .forms import PropertyForm, BuyerSignUpForm, SellerSignUpForm
from django.contrib import messages
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

def register_buyer(request):
    if request.method == 'POST':
        form = BuyerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = BuyerSignUpForm()
    return render(request, 'register_buyer.html', {'form': form})

def register_seller(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = SellerSignUpForm()
    return render(request, 'register_seller.html', {'form': form})


@login_required
def property_list(request):
    query = request.GET.get('q')
    if request.user.is_seller:
        properties = Property.objects.filter(seller=request.user)
    else:
        properties = Property.objects.all()  
    
    if query:
        properties = properties.filter(
            Q(location__icontains=query) | Q(title__icontains=query)
        )
    
    return render(request, 'property_list.html', {'properties': properties, 'query': query})

@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'property_detail.html', {'property': property})

@login_required
def create_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.seller = request.user
            property.save()
            messages.success(request, 'Property listed successfully.')
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyForm()
    return render(request, 'property_form.html', {'form': form})

@login_required
def buy_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        transaction = Transaction.objects.create(
            buyer=request.user,
            property=property,
            amount=property.price
        )
        property.is_sold = True
        property.save()
        messages.success(request, f'Congratulations! You have successfully purchased {property.title}.')
        return redirect('purchase_confirmation', pk=property.pk)
    return render(request, 'buy_property.html', {'property': property})

@login_required
def purchase_confirmation(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'purchase_confirmation.html', {'property': property})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('property_list')
        messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def edit_or_delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = PropertyForm(request.POST, request.FILES, instance=property)
            if form.is_valid():
                form.save()
                messages.success(request, 'Property updated successfully.')
                return redirect('property_detail', pk=property.pk)
        elif 'delete' in request.POST:
            property.delete()
            messages.success(request, 'Property deleted successfully.')
            return redirect('property_list')
    else:
        form = PropertyForm(instance=property)
    
    context = {
        'form': form,
        'property': property,
        'editing': True
    }
    return render(request, 'edit_or_delete_property.html', context)

@login_required
def mark_as_sold(request, pk):
    property = get_object_or_404(Property, pk=pk, seller=request.user)
    if request.method == 'POST':
        property.is_sold = True
        property.save()
        messages.success(request, 'Property marked as sold successfully.')
        return redirect('property_list')
    return render(request, 'mark_as_sold.html', {'property': property})