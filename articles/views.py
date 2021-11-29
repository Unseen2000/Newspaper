from django.shortcuts import render
from django.views.generic import ListView,DetailView,FormView
from django.views.generic.edit import UpdateView,DeleteView,CreateView,FormMixin
from .models import Article
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .forms import CommentForm

class ArticleListView(LoginRequiredMixin,ListView):
    model = Article
    login_url = 'login'
    template_name = 'article_list.html'
    ordering = ['-date']

class ArticleDetailView(LoginRequiredMixin,FormMixin,DetailView):
    model = Article
    template_name = 'article_detail.html'
    login_url = 'login'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('article_detail',args=[str(self.object.id)])
   
    def get_context_data(self,**kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = self.object.comments.all
        return context
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = self.request.user
            comment.article = self.object
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    


class ArticleUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Article
    template_name = 'article_edit.html'
    fields = ('title','body',)
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user 


class ArticleDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Article
    template_name = 'article_delete.html' 
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title','body')
    login_url = 'login'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

