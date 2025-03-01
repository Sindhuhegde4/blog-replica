from django.utils import timezone
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)


# Create your views here.
class AboutView(TemplateView):
    template_name='about.html'

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'


    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'  
    context_object_name = 'post'


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'post_detail.html'
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'  # Adjust this line based on your actual app name



class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name = 'post_detail.html'
    form_class = PostForm
    template_name = 'post_form.html'
    model=Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post 
    template_name = 'post_confirm_delete.html'
    success_url=reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name = 'post_detail.html'
    form_class = PostForm
    template_name = 'post_draft_list.html'
    model=Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(published_date__isnull=True).order_by('created_date')
        return context
    # def get_queryset(self):
    #     print("data,", Post.objects.filter(published_date__isnull=True))
    #     data= Post.objects.filter(published_date__isnull=True).order_by('created_date')
    #     return redirect('post_draft_list',data)


########################################################################################
@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

  
@login_required   
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=CommentForm
    return render(request,'comment_form.html',{'form':form})


@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)







