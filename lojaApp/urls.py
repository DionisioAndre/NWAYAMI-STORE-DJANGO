from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    MyTokenObtainPairView,
    ProductViewSet,
    OrderViewSet,
    ProductUpdateView,
    PublicProductListView,
    SellerOrdersView,
    AdminProductViewSet,
    AdminOrderViewSet,
    AdminUsersViewSet,AdminProductUpdateView,
<<<<<<< HEAD
    SuperUserViewSet,
    criar_fatura, 
    gerar_proforma_pdf
=======
    SuperUserViewSet
>>>>>>> da0259fcee8726afb712a5afe2ca0ec21dfc0994
)
from django.conf import settings
from django.conf.urls.static import static

# Configuração do roteador
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'admin/products', AdminProductViewSet, basename='admin-products')
router.register(r'admin/orders', AdminOrderViewSet, basename='admin-orders')
router.register(r'admin/users', AdminUsersViewSet, basename='admin-users')
router.register(r'admin/ProductUpdate', AdminProductUpdateView, basename='admin-ProductUpdate')
router.register(r'superusers', SuperUserViewSet, basename='superuser')
urlpatterns = [
    path('seller/orders/', SellerOrdersView.as_view(), name='seller_orders'), 
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
<<<<<<< HEAD
    path('api/faturas/', criar_fatura, name='criar_fatura'),
    path('api/faturas/<int:fatura_id>/gerar-proforma/', gerar_proforma_pdf, name='gerar_proforma_pdf'),
=======
>>>>>>> da0259fcee8726afb712a5afe2ca0ec21dfc0994
    path('products/public/', PublicProductListView.as_view(), name='public_product_list'),  
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),  # Nova rota para refresh token
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),  # Rota para atualizar produto
    path('router', include(router.urls)), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
