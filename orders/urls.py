from django.urls    import path

from orders.views   import OrderListView

app_name = 'orders'
urlpatterns = [
    path('', OrderListView.as_view()),
    path('/details/<int:product_id>')
]