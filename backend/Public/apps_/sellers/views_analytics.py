from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps_.sellers.services import SellerAnalyticsService
from apps_.orders.services import AnaliticOrdersService

class SellerAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seller = getattr(request.user, 'seller', None)
        if not seller:
            return Response({'detail': 'Seller not found'}, status=404)
        data = {
            'orders_today': SellerAnalyticsService.get_daily_seller_sales(seller.id),
            'orders_week': SellerAnalyticsService.get_weekly_seller_sales(seller.id),
            'orders_total': SellerAnalyticsService.get_total_seller_sales(seller.id),
            'orders_cancelled': SellerAnalyticsService.get_canceled_seller_orders(seller.id),
        }
        return Response(data)
