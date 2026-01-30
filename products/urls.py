from django.urls import path
from . import views
from reviews import views as review_views

urlpatterns = [
    path("", views.product_list, name="products"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),

    # Admin CRUD
    path("add/", views.add_product, name="add_product"),
    path("edit/<int:product_id>/", views.edit_product, name="edit_product"),
    path("delete/<int:product_id>/", views.delete_product, name="delete_product"),
]



urlpatterns += [
    path("<int:product_id>/reviews/add/", review_views.add_review, name="add_review"),
    path("reviews/<int:review_id>/edit/", review_views.edit_review, name="edit_review"),
    path("reviews/<int:review_id>/delete/", review_views.delete_review, name="delete_review"),
]
