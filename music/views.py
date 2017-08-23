from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from django.http import JsonResponse
from .models import Album
from .forms import UserLogin, ProfileForm, UserForm
from rolepermissions.mixins import HasPermissionsMixin

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

#class AlbumCreate(HasPermissionsMixin, CreateView):
class AlbumCreate(CreateView):
    required_permission = 'add_album'
    model = Album
    fields = ['artist', 'album_title','genre', 'album_logo']

class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title','genre', 'album_logo']

class AlbumDelete(DeleteView):
    model = Album
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        print('vamos bien')
        data = {
            'del': True
        }
        if data['del']:
            data['message'] = 'Borrado'
        print('casi')
        return JsonResponse(data)

class UserFormView(View):
    form_class = ProfileForm
    form_class2 = UserForm
    template_name = 'music/registration_form.html'

    #display blank form
    def get(self,request):
        form = self.form_class(None)
        form2 = self.form_class2(None)
        return render(request,self.template_name,{'form': {form,form2}})

    #process form dta
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        form2 = self.form_class2(request.POST)
        if form2.is_valid() and form.is_valid():
            user = form2.save(commit=False)
            profile = form.save(commit=False)
            role = form.cleaned_data['role']
            #cleaned (normalized) data
            first_name = form2.cleaned_data['first_name']
            last_name = form2.cleaned_data['last_name']
            email = form2.cleaned_data['email']
            password = form2.cleaned_data['password']
            username = form2.cleaned_data['username']
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()
            prof=user.userprofile
            prof.role=role
            prof.avatar=form.cleaned_data['avatar']
            prof.save()


            #return User objetcs if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('music:index')

        return render(request,self.template_name,{'form': {form,form2}})

class LoginView(View):
    form_class = UserLogin
    template_name = 'music/login.html'
    #display blank form
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form': form})
    #process form dta
    def post(self,request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        #return User objetcs if credentials are correct
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('music:index')
        return render(request,self.template_name,{'form': form})

def logout_view(request):
    form = UserLogin(None)
    template_name = 'music/login.html'
    logout(request)
    return render(request,template_name,{'form': form})
