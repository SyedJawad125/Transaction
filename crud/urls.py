from django.urls import path
from .views import ProductView

urlpatterns = [
    path('Product', ProductView.as_view({'get':'fetch', 'post':'create', 'patch':'update', 'delete':'destroy'}))
]

# path('register', RegisterAPIView.as_view({"post": "create"}), name='register'),

# path('department', DepartmentViews.as_view({"get":"get_department",
#                             "post":"post_department",
#                             "patch":"update_department",
#                             "delete":"delete_department"})),
