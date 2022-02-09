from django.urls import path
from .models import Product
from . import views

urlpatterns = [
    
    path('',views.store,name='store'),
    path('catagory/<slug:catagory_slug>/',views.store,name='product_by_catagory'),
    path('catagory/<slug:catagory_slug>/<slug:product_slug>/',views.product_detial,name='product_detial'),
    path('search/',views.search,name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

    
]
#+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
