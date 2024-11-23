
from rest_framework_nested import routers 

from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customer', views.CustomerViewSet)

# >>>>> child based routers
# example products/1/reviews/1
products_router = routers.NestedDefaultRouter(router, 'products', lookup="product")
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup="cart")
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + cart_router.urls


