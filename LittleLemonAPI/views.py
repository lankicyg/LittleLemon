from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view 
from rest_framework.views import APIView

from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage


@api_view(['GET', 'POST'])
def menu_items(request):
     if request.method == 'GET': 
          items = MenuItem.objects.select_related('category').all()
          category_name = request.query_params.get('category')
          to_price = request.query_params.get('to_price')
          search = request.query_params.get('search')
          ordering = request.query_params.get('ordering')
          perpage = request.query_params.get('perpage', default=2)
          page = request.query_params.get('page', default=1)
          if category_name:
               items = items.filter(category__title=category_name)
          if to_price:
               items = items.filter(price__lte=to_price)  #lte: less than or equal to
          if search:
               items = items.filter(title__icontains=search)
          if ordering: 
               ordering_fields = ordering.split(",")
               items = items.order_by(*ordering_fields)
               #items = items.order_by(ordering)

          paginator = Paginator(items, per_page=perpage)
          try:
               items = paginator.page(number=page)
          except EmptyPage:
               items = []
          
          serialized_item = MenuItemSerializer(items, many=True)
          return Response(serialized_item.data)
     if request.method == 'POST':
          serialized_item = MenuItemSerializer(data=request.data)
          serialized_item.is_valid(raise_exception=True)
          serialized_item.save()
          return Response(serialized_item.data, status.HTTP_201_CREATED)


@api_view()
def single_item(request, id):
     item = get_object_or_404(MenuItem, pk=id)
     serialized_item = MenuItemSerializer(item)
     return Response(serialized_item.data)


class CategoriesView(generics.ListCreateAPIView):
     queryset = Category.objects.all()
     serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
     queryset = MenuItem.objects.all()
     serializer_class = MenuItemSerializer
     ordering_fields = ['price', 'inventory']
     filterset_fields = ['price', 'inventory']
     search_fields = ['title']



# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#      queryset = MenuItem.objects.all()
#      serializer_class = MenuItemSerializer



# class BookList(APIView):
#      def get(self, request):
#           author = request.GET.get('author')
#           if (author):
#                return Response({"message": "list of the book by" + author}, status.HTTP_200_OK)
#           return Response({"message": "list of the books"}, status.HTTP_200_OK)

#      def post(self, request):
#           return Response({"title": request.data.get('title')}, status.HTTP_201_CREATED)
     

# class Book(APIView):
#      def get(self, request, pk):
#           return Response({"message": "single book with id" + str(pk)}, status.HTTP_200_OK)
     
#      def put(self, request, pk):
#           return Response({"title": request.data.get('title')}, status.HTTP_200_OK)