
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps_.users.services import UserAnalyticsService
from apps_.sellers.services import SellerAnalyticsService
from apps_.products.services import ProductAnalyticsService
from apps_.orders.services import AnaliticOrdersService
from apps_.payments.services import PaymentAnalyticsService
from config.permissions import IsSeller, IsAdmin

class AdminAnalyticsView(APIView):
	permission_classes = [IsAdmin]

	def get(self, request):
		data = {
			'users': {
				'total': UserAnalyticsService.get_total_users(),
				'active_dau': UserAnalyticsService.get_active_users_dau(),
				'active_mau': UserAnalyticsService.get_active_users_mau(),
				'registrations_today': UserAnalyticsService.get_daily_registrations(),
			},
			'sellers': {
				'total': SellerAnalyticsService.get_total_sellers(),
				'active': SellerAnalyticsService.get_active_sellers(),
				'pending_verification': SellerAnalyticsService.get_pending_verification_sellers(),
			},
			'products': {
				'total': ProductAnalyticsService.get_total_products(),
				'out_of_stock': ProductAnalyticsService.get_out_of_stock_count(),
				'by_category': list(ProductAnalyticsService.get_product_count_by_category()),
			},
			'orders': {
				'per_day': AnaliticOrdersService.get_orders_per_day(),
				'pending': AnaliticOrdersService.get_pending_count(),
				'cancelled': AnaliticOrdersService.get_cancelled_count(),
				'completed': AnaliticOrdersService.get_completed_count(),
			},
			'payments': {
				'success_vs_failed': PaymentAnalyticsService.get_success_vs_failed_payments(),
			},
		}
		return Response(data)

