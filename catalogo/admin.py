from django.contrib import admin
from catalogo.models import Livro, Autor, Genero, InstanciaLivro

# Register your models here.
# Define the admin class

class LivroInline(admin.TabularInline):
    model = Livro

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = [
        'first_name',
        'last_name',
        ('date_of_birth', 'date_of_death')
        ]
    inlines = [LivroInline]
    

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    pass


# Registre as classes de Admin para BookInstance usando o decorador
@admin.register(InstanciaLivro)
class InstanciaLivroAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back', 'borrower', 'id', 'livro')

    fieldsets = (
        (None, {
            'fields': ('livro', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

class BooksInstanceInline(admin.TabularInline):
    model = InstanciaLivro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'display_genero')
    inlines = [BooksInstanceInline]

# admin.site.register(Autor)
# admin.site.register(Genero)
# admin.site.register(InstanciaLivro)