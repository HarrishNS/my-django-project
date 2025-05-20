from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post
from accounts.models import UserProfile

class PublicPostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'  # Create this template
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            user__userprofile__is_private=False
        ).order_by('-created_at')


class UserPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'caption']
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post-list')  # Replace with your list view URL name

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')
    template_name = 'posts/post_confirm_delete.html'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

# Create your views here.
