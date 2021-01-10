from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date



import uuid # Obrigatório para instâncias de livro exclusivas

# Create your models here.
class Genero(models.Model):
    """
    Modelo que representa um gênero de livro.
    """

    name = models.CharField(max_length=200, help_text='Insira o gênero de um livro (por exemplo, ficção científica)')

    def __str__(self):
        """String para representar o Modelo de objeto."""
        return self.name

class Livro(models.Model):
    """
    Modelo que representa um livro (mas não uma cópia específica de um livro).
    """
    titulo = models.CharField(max_length=200)
    # Chave estrangeira usada porque o livro pode ter apenas um autor, mas os autores podem ter vários livros
    # Autor como uma string em vez de um objeto porque ainda não foi declarado no arquivo
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    #summary
    resumo = models.TextField(max_length=1000, help_text='Insira uma breve descrição do livro')
    isbn = models.CharField(
        'ISBN', max_length=13,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
        )
    # ManyToManyField usado porque o gênero pode conter muitos livros. Os livros podem abranger muitos gêneros.
    # A classe de gênero já foi definida para que possamos especificar o objeto acima.
    genero = models.ManyToManyField(
        Genero, help_text='Selecione um gênero para este livro'
        )

    def __str__(self):
        """String for representing the Model object."""
        return self.titulo
    def get_absolute_url(self):
        """Retorna o url para acessar um registro de detalhes deste livro."""
        return reverse('book-detail', args=[str(self.id)])
    def display_genero(self):
        """
        Crie uma string para o Gênero. Isso é necessário para exibir o gênero no Admin.
        """
        return ', '.join(genero.name for genero in self.genero.all()[:3])

    display_genero.short_description = 'Genero'



class InstanciaLivro(models.Model):
    """
    Modelo que representa uma cópia específica de um livro (ou seja, que pode ser emprestado da biblioteca).
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='ID exclusivo para este livro específico em toda a biblioteca'
        )
    livro = models.ForeignKey('Livro', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    STATUS_EMPRESTIMO = (
        ('M', 'Manutenção'),
        ('E', 'Por empréstimo'),
        ('A', 'Acessível'),
        ('R', 'Reservado'),
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_EMPRESTIMO,
        blank=True,
        default='m',
        help_text='Disponibilidade de livros',
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.livro.titulo})'
    @property
    def is_overdue(self):
        # se uma determinada instância do livro está atrasada. 
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Autor(models.Model):
    """
    Modelo que representa um autor.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'



