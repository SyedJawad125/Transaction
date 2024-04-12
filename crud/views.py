from rest_framework.viewsets import ModelViewSet
from .controller import ProductController


product_controller = ProductController()

class ProductView(ModelViewSet):

    def create(self, request):
        return product_controller.create_product(request)

    def fetch(self, request):
        return product_controller.fetch_product(request)

    def update(self, request):
        return product_controller.update_product(request)

    def destroy(self, request):
        return product_controller.destroy_product(request)
