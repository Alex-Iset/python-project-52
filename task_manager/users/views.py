from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.users.forms import UserCreateForm, UserUpdateForm
from task_manager.users.constants import SUCCESS_MESSAGES, ERROR_MESSAGES


class UserPermissionMixin(LoginRequiredMixin):
    error_message = ERROR_MESSAGES['no_permission']
    login_required_message = ERROR_MESSAGES['not_authenticated']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.login_required_message)
            return redirect(reverse_lazy('login'))

        if request.user.pk != kwargs.get('pk'):
            messages.error(request, self.error_message)
            return redirect(reverse_lazy('users_list'))

        return super().dispatch(request, *args, **kwargs)


class UsersListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    paginate_by = 7
    ordering = ['-date_joined']


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = SUCCESS_MESSAGES['user_created']


class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = SUCCESS_MESSAGES['user_updated']
    error_message = ERROR_MESSAGES['no_permission_update']


class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')
    success_message = SUCCESS_MESSAGES['user_deleted']
    error_message = ERROR_MESSAGES['no_permission_update']

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user.tasks.exists():
            messages.error(request, ERROR_MESSAGES['user_has_tasks'])
            return redirect(self.success_url)

        return super().delete(request, *args, **kwargs)


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name='users/auth/login.html'
    redirect_authenticated_user = True
    success_message = SUCCESS_MESSAGES['logged_in']
    error_message = ERROR_MESSAGES['login_invalid']

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class UserLogoutView(SuccessMessageMixin, LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, SUCCESS_MESSAGES['logged_out'])
        return super().dispatch(request, *args, **kwargs)
