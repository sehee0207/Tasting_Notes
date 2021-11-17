# from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse
from django.utils import timezone
from .models import Photo, Comment
from .forms import CommentForm
# Create your views here.

class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'

class PhotoCreate(CreateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_create'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})
    
class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'
    
    def dispatch(self, request, *args, **kwargs) :
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)
        
from django.http import HttpResponseRedirect
from django.contrib import messages

class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'
    
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'

class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
                    
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
        
class Photofavorite(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.favorite.all():
                    photo.favorite.remove(user)
                else:
                    photo.favorite.add(user)
            return HttpResponseRedirect('/')
        
class PhotoLikeList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인을 먼저 하세요')
            return HttpResponseRedirect('/')
        return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        queryset = user.like_post.all()
        return queryset
    
class PhotoFavoriteList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인을 먼저 하세요')
            return HttpResponseRedirect('/')
        return super(PhotoFavoriteList, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset
    
class PhotoMyList(ListView):
    model = Photo
    template_name = 'photo/photo_mylist.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인을 먼저 하세요')
            return HttpResponseRedirect('/')
        return super(PhotoMyList, self).dispatch(request, *args, **kwargs)
    
    
@login_required(login_url='accounts:login')
def comment_create_photo(request, photo_id):
    """
    photo 질문댓글등록
    """
    photo = get_object_or_404(Photo, pk=photo_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.photo = photo
            comment.save()
            return redirect('photo:detail', pk=photo.id)
            # return HttpResponseRedirect('/')
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'photo/comment_form.html', context)

@login_required(login_url='accounts:login')
def comment_modify_photo(request, comment_id):
    """
    photo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('photo:detail', pk=comment.photo.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('photo:detail', pk=comment.photo.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'photo/comment_form.html', context)

@login_required(login_url='accounts:login')
def comment_delete_photo(request, comment_id):
    """
    photo 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('photo:detail', pk=comment.photo.id)
    else:
        comment.delete()
    return redirect('photo:detail', pk=comment.photo.id)