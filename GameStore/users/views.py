from django.shortcuts import redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView
from django.urls import reverse_lazy
from .forms import LoginUserForm, RegisterUserForm,CustomPasswordChangeForm,ProfileEditForm,CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginUser(LoginView):
    form_class = LoginUserForm 
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home') 

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'} 
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return response

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Смена пароля'}

class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
    extra_context = {'title': 'Пароль изменен'}

class LogoutUser(LogoutView):
    next_page = 'home'

class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль пользователя'
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileEditForm
    template_name = 'users/profile_edit.html'
    
    def get_object(self):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy('users:profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context
    
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')
    extra_context = {'title': 'Восстановление пароля'}

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    extra_context = {'title': 'Письмо отправлено'}

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    extra_context = {'title': 'Ввод нового пароля'}

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    extra_context = {'title': 'Пароль восстановлен'}