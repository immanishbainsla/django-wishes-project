from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth import get_user_model

from .models import UserWishListModel
from .forms import UserLogInForm, UserSignUpForm, UserWishListForm, UserContactForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

# HOME PAGE VIEW
def index(request):
    return render(request, 'index.html')


# USER SIGN UP VIEW
def register(request):
    # loginform = UserLogInForm()
    if request.method == 'POST':
        form = UserSignUpForm(data = request.POST)

        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            messages.success(request, 'Account has been created, now you need to Login.')
            # return render(request, 'user_login', context={'form':loginform})
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(request,'Form in Invalid.')

    else:
        form = UserSignUpForm()

    return render(request, 'wishlist/signup.html', context={'form':form})

# class SignUp(CreateView):
#     form_class = UserSignUpForm
#     success_url = reverse_lazy("login")
#     template_name = "accounts/signup.html"


# USER LOGIN VIEW
def user_login(request):
    form = UserLogInForm(data=request.POST)
    if request.method == 'POST':
        # if form.is_valid():
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                # messages.error(request, 'Sorry, this ACCOUNT is not ACTIVE.')
                return HttpResponse("Your account is not active.")
        else:
            # messages.error(request, 'Account doesnt EXIST.')
            return HttpResponse("Invalid login details supplied.")
    else:
        form = UserLogInForm()
    return render(request, 'wishlist/login.html', context={'form':form})


    # else:
    #     form = UserLogInForm()
    # return render(request, 'wishlist/login.html', context={'form':form})


# USER LOGOUT VIEW
@login_required(login_url = '/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# USER CONTACT VIEW
def contactview(request):
    if request.method == 'POST':
        form = UserContactForm(data = request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'We have recieved your Query. We will contact you soon. Thanks.')

        else:
            messages.error(request, 'Form in Invalid.')

    else:
        form = UserContactForm()

    return render(request, 'wishlist/contact.html', context={'form':form})


class AboutView(TemplateView):
    template_name = 'wishlist/about.html'


class UserWishListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = UserWishListModel
    context_object_name = 'wishes'
    template_name = 'wishlist/userwishlist.html'

    def get_queryset(self):
        return UserWishListModel.objects.filter(user=self.request.user)

    # def get_context_data(self, **kwargs):
    #     userwishlists = self.get_queryset() # .title
    #     context = super(UserWishListView, self).get_context_data(**kwargs)
    #     context["user_wishlists"] = userwishlists
    #     return context


# @login_required(login_url = '/login/')
# def UserWishListDetailView(request):
#     user_wishlists = UserWishListModel.objects.all().filter(user_id=self.user_id)
#     redirect_field_name = 'redirect_to'
#     model = UserWishListModel
#



class UserWishListDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = UserWishListModel
    context_object_name = 'wishlist_details'
    template_name = 'wishlist/userwishlistdetail.html'

    # def get(request):
    #     if not user.is_authenticated:
    #         return render(request, 'user_login')
    #     else:
    #         return render(request, template_name, context={'pk':pk})



@login_required(login_url = '/login/')
def CreateWishListView(request):
    # Change here  get_user_model()
    user = User
    form = UserWishListForm(request.POST)
    if request.method == 'POST':
        form = UserWishListForm(request.POST)
        if form.is_valid():
            d = form.save(commit=False)
            a = request.user
            # a.id
            d.user_id   = a.id
            print(a.username)
            d.save()
            return redirect('wishlist:wishlist')

        else:
            form = UserWishListForm()
    return render(request,'wishlist/addwishlist.html', context={'form':form})


# class CreateWishListView(CreateView, LoginRequiredMixin):
#     model = UserWishListModel
#     fields = ("title","description")
#     template_name = 'wishlist/addwishlist.html'
#     # success_url = reverse_lazy("wishlist/userwishlistdetail.html")
#     user = get_user_model()

     # def post(self,request):
         # if request.user.is_authenticated:
             # self.user.save(request.user)

     # def post(self,request):
         # form = UserWishListForm(data=request.POST)
         # if form.is_valid():
             # newwish = form.save(commit=False) # Save topic in a variable.
             # newwish.owner = request.user # Set topics owner attribute to current user.
             # newwish.save() # Save the changes to the database.
             # return HttpResponseRedirect(reverse('wishlist:detail'))


class WishListUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = UserWishListModel
    fields = ("title","description")
    template_name = 'wishlist/addwishlist.html'



class WishListDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = UserWishListModel
    template_name = 'wishlist/deletewishlist.html'
    context_object_name = 'wishlist_details'
    success_url = reverse_lazy('wishlist:wishlist')

    # def get_object(self, queryset=None):
    #     """ Hook to ensure object is owned by request.user. """
    #     obj = super(WishListDeleteView, self).get_object()
    #     if not obj.user == self.request.user:
    #         raise Http404
    #     return obj.delete()

    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     self.object.delete()
    #     return HttpResponseRedirect(success_url)
    #
    # def get_success_url(self):
    #     if self.success_url:
    #         return self.success_url.format(**self.object.__dict__)
    #     else:
    #         raise ImproperlyConfigured(
    #             "No URL to redirect to. Provide a success_url.")
