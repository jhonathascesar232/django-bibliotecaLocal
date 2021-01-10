from django.shortcuts import render
from catalogo.models import Livro, Autor, InstanciaLivro, Genero


# Create your views here.
def index(request):
    """View function for home page of site."""

    # Gerar contagens de alguns dos objetos principais
    num_books = Livro.objects.all().count()
    num_instances = InstanciaLivro.objects.all().count()
    # Livros disponíveis (status = 'a')
    num_instances_available = InstanciaLivro.objects.filter(status__exact='A').count()
    # O 'all ()' é implícito por padrão.
    num_authors = Autor.objects.count()
    num_genres = Genero.objects.all().count()

    # Número de visitas a esta view, conforme contado na variável de sessão.
    num_visits = request.session.get('num_visits', 1) # busca 'num_visits' se vazio retorna 1
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,

    }
    # Renderize o template HTML index.html com os dados na variável de contexto
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Livro
    # context_object_name  = 'my_book_list' # seu próprio nome para a lista como uma variável de modelo
    # queryset = Livro.objects.filter(titulo__icontains='Mil')[:5] # Obtenha 5 livros contendo 'guerra' no título
    # Especifique seu próprio nome / local de modelo
    template_name = 'catalog/book_list.html'
    paginate_by = 2


    def get_context_data(self, **kwargs):
        # Chame a implementação de base primeiro para obter o contexto
        context = super(BookListView, self).get_context_data(**kwargs)
        # Crie quaisquer dados e adicione-os ao contexto
        context['some_data'] = 'Estes são apenas alguns dados'
        return context
    def get_queryset(self):
        return Livro.objects.all()
        # return Livro.objects.filter(titulo__icontains='Mil')[:2]

from django.shortcuts import get_object_or_404

class BookDetailView(generic.DetailView):
    model = Livro
    template_name = 'catalog/book_detail.html'
    # context_object_name  = 'author'
    

    
    # queryset = Livro.objects.all()

    # def get_queryset(self, *args, **kwargs):
    #     return Livro.objects.filter(pk=self.kwargs['pk'])
    # def get_queryset(self):
    #     obj = super().get_object()
    #     obj = Livro.objects.get(pk=self.kwargs["pk"])

        # return obj
    # def get_object(self):
    #     return Livro.objects.get(pk=self.kwargs['pk'])
    # def get(self, request, pk):
    #     self.context = Livro.objects.get(pk=pk)
        
        
        
    # def get_object(self, pk):
    #     obj = super().get_object()
    #     # Record the last accessed date
    #     return obj

def book_detail_view(request, pk):
    book = get_object_or_404(Livro, pk=pk)
    return render(request, 'catalog/book_detail.html', context={'book': book})

# view baseadas em classe
class AuthorListView(generic.ListView): # 1 uma classe para view in lista
    model = Autor                       # na page a variavel e autor
    template_name = 'catalog/author_list.html'
    paginate_by = 2
    def get_context_data(self, **kwargs):
        # Chame a implementação de base primeiro para obter o contexto
        context = super(AuthorListView, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Autor.objects.all()

class AuthorDetailView(generic.DetailView): # 2 classe para detalhes
    model = Autor   
    template_name = 'catalog/author_detail.html'

def author_detail_view(request, pk):
    author = get_object_or_404(Autor, pk=pk)
    books =Livro.objects.filter(autor__pk=pk)

    return render(request, 'catalog/author_detail.html', context={'author': author, 'books':books})


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    'Generic class-based view' que lista livros emprestados ao usuário atual.
    """
    model = InstanciaLivro
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return InstanciaLivro.objects.filter(borrower=self.request.user).filter(status__exact='E').order_by('due_back')


from django.contrib.auth.mixins import PermissionRequiredMixin

class BibliotecaBooksByUserListView(PermissionRequiredMixin, generic.ListView):
    """
    'Generic class-based view' que lista livros emprestados ao usuário atual.
    """
    model = InstanciaLivro
    template_name = 'catalog/book_list_biblioteca.html'
    # Or multiple permissions
    permission_required = 'catalogo.can_mark_returned'
    paginate_by = 2

    def get_queryset(self):
        return InstanciaLivro.objects.filter(status__exact='E').order_by('due_back')


import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalogo.forms import RenewBookForm

@login_required
@permission_required('catalogo.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """
    Função de visualização para renovar um BookInstance específico pelo bibliotecário.
    """
    book_instance = get_object_or_404(InstanciaLivro, pk=pk)
    # Se esta for uma solicitação POST, processe os dados do formulário
    if request.method == 'POST':
        # Crie uma instância de formulário e preencha-a com os dados da solicitação (binding):
        form = RenewBookForm(request.POST)
        # Verifique se o formulário é válido:
        if form.is_valid():
            # processe os dados em form.cleaned_data conforme necessário (aqui, apenas os gravamos no campo due_back do modelo)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            # redirect to a new URL name:
            return redirect('b-books')
    # Se este for um GET (ou qualquer outro método), crie o formulário padrão.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)




from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalogo.models import Autor
from catalogo.forms import AutorForm

class AuthorCreate(CreateView):
    model = Autor
    # fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    form_class = AutorForm
    initial = {'date_of_death': '11/06/2020'}
    template_name = 'catalog/author_form.html'
    
class AuthorUpdate(UpdateView):
    model = Autor
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
class AuthorDelete(DeleteView):
    model = Autor
    success_url = reverse_lazy('authors')



from django.views.generic.edit import CreateView
from catalogo.forms import BookForm

class BookCreate(CreateView):
    template_name = 'catalog/book_form.html'
    model = Livro
    form_class = BookForm
    # fieldsets = (

    # )
    # fields = ('titulo', 'autor', 'resumo','isbn', 'genero')

     # self.fields['titulo'].widget.attrs.update({'class': 'form-control'})


    # fields = ['titulo', 'autor', 'resumo', 'isbn', 'genero']


from django.views.generic.edit import UpdateView, DeleteView
from catalogo.forms import BookForm
from django.urls import reverse_lazy

class BookUpdate(UpdateView):
    template_name = 'catalog/book_form.html'
    model = Livro
    form_class = BookForm

class BookrDelete(DeleteView):
    template_name = 'catalog/book_confirm_delete.html'
    model = Livro
    # reverse_lazy retorna para a url name
    success_url = reverse_lazy('books')