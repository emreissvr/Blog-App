from django.contrib import admin
from .models import Article,Comment

admin.site.register(Comment)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin): 

    # ModelAdmin classındaki özelliklerden birkaçı kullanıldı
    list_display = ["title","author","createdDate"]    

    list_display_links = ["title","createdDate"]

    search_fields = ["title"]
    
    list_filter = ["title"] 
    
    class Meta:
        model = Article
