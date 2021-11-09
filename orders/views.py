import json
import uuid

from django.views       import View
from django.http        import JsonResponse
from json.decoder       import JSONDecodeError

from orders.models      import Order
from products.models    import ProductOption
from core.utils         import login_required

class OrderListView(View):
    @login_required
    def get(self, request):
        results = [{
            "id"                  : order.id,
            "order_number"        : order.order_number,
            "status"              : order.order_status.name,
            "shipping_address"    : order.shipping_address,
            "product_id"          : order.product_option.product.id,
            "user_id"             : order.user_id,
            "product_title"       : order.product_option.product.title,
            "serial"              : order.product_option.product.serial,
            "size"                : order.product_option.size.type,
            "quantity"            : order.quantity,
            "price"               : order.price,
            "thumbnail_image_url" : order.product_option.product.thumbnail_image_url,
        } for order in Order.objects.filter(user_id=request.user.id)\
                                    .select_related('product_option__product', 'product_option__size', 'order_status')]

        return JsonResponse({"results" : results}, status=200)
        
    @login_required
    def post(self, request):
        try:
            data_list = json.loads(request.body)
            for data in data_list:
                order_number   = uuid.uuid4()
                product_option = ProductOption.objects.get(product_id=data['product_id'], size__type=data['size'])

                Order.objects.create(
                    user_id           = request.user.id,
                    product_option_id = product_option.id,
                    quantity          = data['quantity'],
                    price             = data['price'],
                    order_number      = order_number,
                    order_status_id   = '2',                # 주문완료
                    shipping_address  = data['address'],
                )
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except ProductOption.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST_PRODUCT_OPTION"}, status=400)