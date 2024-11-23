from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, DjangoModelPermissions

from store.filters import ProductFilter
from store.pagination import DefaultPagination
from store.permissions import DjangoAdminFullPermissions, IsAdminOrReadOnly

from .models import Cart, CartItem, Collection, Customer, Product, OrderItem, Reviews
from .serializers import CollectionSerializer, CustomUserSerializer, ProductSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer

# >>> Model view set 
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination

    # >>>>>> generic filters
    # filterset_fields =  ['collection_id', 'unit_price']

    # >>>>>> custom filter
    filterset_class = ProductFilter

    # >>>>> in build permissions
    # permission_classes = [IsAuthenticated]

    # >>>>>> custom permission
    permission_classes = [IsAdminOrReadOnly]

    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', "last_update"]

    # >>>>>> customise permission function
    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
    
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product=kwargs['pk']).count() > 0:
            return Response(
                {"error": "Product cannot be deleted as it is associated with an order item"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)
    

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response(
                {"error": "Collection cannot be deleted as it have associated product items."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    # queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Reviews.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    

# >>>> mixin based api's
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class =  CartSerializer 


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self):
        return CartItem.objects\
                    .filter(cart=self.kwargs['cart_pk'])\
                    .select_related('product')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomUserSerializer
    # >>>> Model based permission
    # permission_classes = [DjangoModelPermissions]

    permission_classes = [IsAdminUser]

    # >>>> Custom model permission
    # permission_classes = [DjangoAdminFullPermissions]

    # >>>>>> override class permission on a specific action
    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer, created = Customer.objects.get_or_create(user=request.user)
        if request.method == 'GET':
            serializer = CustomUserSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomUserSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        



