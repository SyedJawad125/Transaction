from django.db import transaction
from .serializers import *
from utils.helper import *
from utils.response_messages import *

class ProductController:
    product_serializer = ProductSerializer
    image_serializer = ImagesSerializer

    def create_product(self, request):
        try:
            serialized_product = self.product_serializer(data=request.data)

            if serialized_product.is_valid():
                with transaction.atomic():
                    response_data = serialized_product.save()

                    if "images" in request.data:
                        for i in request.data.getlist('images'):
                            image = {
                                'product': response_data.id,
                                'image': i
                            }
                            serialized_image = self.image_serializer(data=image)
                            if serialized_image.is_valid():
                                serialized_image.save()
                            else:
                                transaction.set_rollback(True)
                                return create_response({}, get_first_error_message_from_serializer_errors(
                                    serialized_image.errors, UNSUCCESSFUL), 400)

                return create_response(self.product_serializer(response_data).data, SUCCESSFUL, 200)
            else:
                return create_response({}, get_first_error_message_from_serializer_errors(
                    serialized_product.errors, UNSUCCESSFUL), 400)

        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)


    def fetch_product(self, request):
        try:
            instances = self.product_serializer.Meta.model.objects.all()
            response_data = self.product_serializer(instances).data
            return create_response(response_data, SUCCESSFUL, 200)

        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)


     # instances = Department.objects.filter(**kwargs)
            # data, count = paginate_data(instances, request)
            # serialized_instances = DepartmentSerializer(data, many=True).data

            # response_data = {
            #         "count": count,
            #         "data": serialized_instances
            #     }

            # return Response(response_data, 200)

    def update_product(self, request):
        try:
            if "id" in request.data:
                instance = self.product_serializer.Meta.model.objects.filter(id=request.data.get('id')).first()
                if instance:
                    serialized_product = self.product_serializer(instance, data=request.data, partial=True)
                    if serialized_product.is_valid():
                        with transaction.atomic():
                            response_data = serialized_product.save()

                            #Frontend will send IDs of images in array, which they want to delete
                            if "delete_images" in request.data and request.data.get('delete_images') != '':
                                kwargs = {}
                                kwargs = get_params('id', request.data.get('delete_images'), kwargs)
                                images_to_delete = self.image_serializer.Meta.model.objects.filter(**kwargs)
                                images_to_delete.delete()

                            if "images" in request.data:
                                for i in request.data.getlist('images'):
                                    image = {
                                        'product': response_data.id,
                                        'image': i
                                    }
                                    serialized_image = self.image_serializer(data=image)
                                    if serialized_image.is_valid():
                                        serialized_image.save()
                                    else:
                                        return create_response({}, get_first_error_message_from_serializer_errors(
                                            serialized_image.errors, UNSUCCESSFUL), 400)
                        return create_response(self.product_serializer(response_data).data, SUCCESSFUL, 200)
                    else:
                        return create_response({}, get_first_error_message_from_serializer_errors(
                            serialized_product.errors, UNSUCCESSFUL), 400)
                else:
                    return create_response({}, NOT_FOUND, 404)
            else:
                return create_response({}, ID_NOT_PROVIDED, 400)

        except Exception as e:
            return create_response({'error': str(e)}, UNSUCCESSFUL, 500)


    def destroy_product(self, request):
        try:
            if "id" in request.query_params:
                instance = self.product_serializer.Meta.model.objects.filter(id=request.query_params.get('id')).first()
                if instance:
                    instance_images = instance.product_images.all()
                    with transaction.atomic():
                        for image in instance_images:
                            image.delete()
                        instance.delete()
                    return create_response({}, SUCCESSFUL, 200)
                else:
                    return create_response({}, NOT_FOUND, 404)
            else:
                return create_response({}, ID_NOT_PROVIDED, 400)

        except Exception as e:
            return create_response({'error': str(e)}, UNSUCCESSFUL, 500)