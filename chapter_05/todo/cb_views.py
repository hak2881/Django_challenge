from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from todo.models import Todo
from django.db.models.query_utils import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class TodoListView(LoginRequiredMixin,ListView):
    model = Todo
    template_name = 'todo_list.html'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo = self.object # pk
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



