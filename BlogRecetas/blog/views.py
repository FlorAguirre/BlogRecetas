from django.shortcuts import render, get_object_or_404
from blog.models import Category, Article
from django.shortcuts import render,HttpResponse, redirect
from blog.forms import ArtForm
from django.contrib import messages





# Create your views here.

def articles(request):

    articles = Article.objects.all()
    
    return render(request,'articles/list.html',{
        'title' : 'Artículos',
        'articles' : articles,
    })


def category(request, category_id):

    category = get_object_or_404(Category, id=category_id)
    articles = Article.objects.filter(categories = category_id)

    
    return render(request,'categories/category.html',{
        'category' : category,
        'articles' :articles
    })

def article(request, article_id):

    article = get_object_or_404(Article, id =article_id)

    return render(request, 'articles/detail.html',{
        'article' : article
    })




# def crear_articulo(request,title,content,public):
#     articulo = Article(
#         title = title,
#         content = content,
#         public = public
#     )


def save_article(request):

    if request.method == 'POST':

        title = request.POST['title']
        content = request.POST['content']
        public = request.POST['public']
    




        articulo = Article(
            title = title,
            content = content,
            public = public,

           
          
        )

        articulo.save()
        return HttpResponse(f'Receta creada:<strong>{articulo.title}')
    
    else:
        return HttpResponse("<h2> No se ha podido crear la receta</h2>")

    

def create_article(request):

    return render(request,'articles/create_article.html')


def create_full_article(request):
    articulo = None # Crear la variable articulo fuera del bloque condicional
    if request.method == "POST":
        formulario = ArtForm(request.POST)
        if formulario.is_valid():
            # Extraer los campos del formulario
            title = formulario.cleaned_data.get('title')
            content = formulario.cleaned_data.get('content')
            public = formulario.cleaned_data.get('public')
            category_ids = request.POST.getlist('categories') # obtener la lista de los ids de categorías seleccionadas
            categories = Category.objects.filter(id__in=category_ids)

  

            # Crear el articulo
            articulo = Article(
                title = title,
                content = content,
                public = public,
                
            )
            articulo.save()
            articulo.categories.set(categories)

            # Crear mensaje flash (sesión que solo se muestra 1 vez)
            messages.success(request,f'Se ha guardado correctamente la receta: {articulo.title}')
            return redirect('list_articles')
    else:
        formulario = ArtForm()
    return render(request, 'articles/create_full_article.html',{
        'form' : formulario
    })


def busqueda_articulo(request):
    return render(request,'articles/buscar_articulo.html')



def buscar(request):

    if request.POST['title']:

        articulo = request.POST['title']
        articulos = Article.objects.filter(title__icontains= articulo)

        return render(request,"articles/resultados_busqueda.html",{"articulos":articulos})
    
    else:
        respuesta = "No enviaste datos"


    return HttpResponse(respuesta)
    

"""
class RecetaCreateView(CreateView):
        model = Article
        template_name = 'articles/create_article.html'
        form_class = ArtForm
        success_url = '.'

        """
