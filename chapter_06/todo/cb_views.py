from django.http.response import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from todo.models import Todo, Comment
from django.db.models.query_utils import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from todo.form import CommentForm

class TodoListView(LoginRequiredMixin,ListView):
    model = Todo
    template_name = 'todo_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(author=self.request.user)

        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)|
                Q(description__icontains=q)
            )
        return queryset

class TodoDetailView(LoginRequiredMixin,DetailView):
    model = Todo
    template_name = 'todo_info.html'
    paginate_by = 10



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        todo = self.object # pk
        context['comments'] = self.object.comments.prefetch_related('author').all()

        context['data'] = {
            'title': todo.title,
            'description': todo.description,
            'created_at': todo.created_at,
            'start_date': todo.start_date,
            'end_date': todo.end_date,
            'modified_at': todo.modified_at,
            'is_completed': todo.is_completed,
        }
        return context

    def post(self, *args, **kwargs):
        comment_form = CommentForm(self.request.POST)
        self.object = self.get_object()  # 디테일에서 제공하는 메서드로 객체 가져오기

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.todo = self.object
            comment.author = self.request.user
            comment.todo_id = self.kwargs['pk']
            comment.save()

            return HttpResponseRedirect(reverse_lazy('todo:info', kwargs={'pk': self.object.pk}))

        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)



class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo_create.html'
    fields =['title', 'description','start_date','end_date']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'pk': self.object.pk})

class TodoUpdateView(LoginRequiredMixin, UpdateView):

    model = Todo
    template_name = 'todo_update.html'
    fields = ['title','description']
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_staff:
            return queryset
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'pk':self.object.pk})

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    def get_queryset(self):
        queryset= super().get_queryset()

        if not self.request.user.is_staff:
            return queryset.filter(author=self.request.user)
        return queryset


    def get_success_url(self):
        return reverse_lazy('todo:list')


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'comment_form.html'
    fields = ['content']

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user :
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'pk': self.object.todo.pk})
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['sub_title'] ='수정'
        context['btn_name'] ='수정'
        return context

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy("todo:info", kwargs={"pk": self.object.todo.pk})