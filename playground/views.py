
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max, Min, Count, Avg, Sum, Func, F, Value, ExpressionWrapper, DecimalField
from store.models import Customer, OrderItem, Product, Order
from django.contrib.contenttypes.models import ContentType

from tags.models import TagItem

# Create your views here.
def hello(request):
    queryset = TagItem.objects.get_tags_for_model(Product, 1)
    print(queryset)
    return render(request, 'hello.html', {'product': queryset})