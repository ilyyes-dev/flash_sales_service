#rmzyy l3ziiiz tahyaa jma3t vim ri thala brk
#rmzy mtba9ch tgouli 3lah 5dmt bel view sets
import hashlib
import json
from django.db import transaction
from django.db.models import F, Q
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import IdempotencyKey, Order, Product
from .serializers import ( OrderResponseSerializer, OrderSerializer, ProductSerializer, ProductStockSerializer,
)


class BrowseProductsView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        q = Product.objects.all().order_by("id")
        params = self.request.query_params

        search = params.get("q")
        if search:
            q = q.filter(Q(name__icontains=search) | Q(description__icontains=search))

        product_id = params.get("id")
        if product_id:
            q = q.filter(id=product_id)

        name = params.get("name")
        if name:
            q = q.filter(name__icontains=name)

        description = params.get("description")
        if description:
            q = q.filter(description__icontains=description)

        price = params.get("price")
        if price:
            q = q.filter(price=price)

        return q


class ProductStockView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductStockSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"
    lookup_url_kwarg = "id"


class MyOrdersView(ListAPIView):
    serializer_class = OrderResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.filter(owner=self.request.user)
            .select_related("product")
            .order_by("-created_at")
        )


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        key = request.headers.get("Idempotency-Key")
        if not key:
            return Response(
                {"Idempotency-Key is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        request_hash = hashlib.sha256(
            json.dumps(
                {"product": product.pk, "quantity": quantity},  
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()       #hadi bch n9dr ncree identifier lel request bch  tjini easy nmanager wncompari requests

        with transaction.atomic():
            obj = IdempotencyKey.objects.filter(user=request.user, key=key)
            if obj:
                if obj.request_hash != request_hash:
                    return Response(
                        {"This key was used for a different request."},
                        status=status.HTTP_409_CONFLICT,
                    )
                return Response(obj.response_body, status=obj.response_status)

            updated_rows = Product.objects.filter(
                pk=product.pk,
                stock__gte=quantity,
            ).update(stock=F("stock") - quantity)

            if updated_rows == 0:
                if not Product.objects.filter(pk=product.pk).exists():
                    raise NotFound("Product not found.")
                raise ValidationError({"Not enough stock available."})

            order = Order.objects.create(
                owner=request.user,
                product=product,
                quantity=quantity,
            )
            response_body = OrderResponseSerializer(order).data
            IdempotencyKey.objects.create(
                user=request.user,
                key=key,
                request_hash=request_hash,
                response_body=response_body,
                response_status=status.HTTP_201_CREATED,
            )

        return Response(response_body, status=status.HTTP_201_CREATED)
