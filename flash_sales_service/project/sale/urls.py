from django.urls import path

from .views import BrowseProductsView, MyOrdersView, PlaceOrderView, ProductStockView

urlpatterns = [
    path("products/", BrowseProductsView.as_view(), name="browse-products"),
    path("products/<int:id>/stock/", ProductStockView.as_view(), name="product-stock"),
    path("orders/", MyOrdersView.as_view(), name="my-orders"),
    path("orders/place/", PlaceOrderView.as_view(), name="place-order"),
]
