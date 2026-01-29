from reviews import views as review_views
from django.urls import path

urlpatterns = [
    path("<int:product_id>/reviews/add/", review_views.add_review, name="add_review"),
    path("reviews/<int:review_id>/edit/", review_views.edit_review, name="edit_review"),
    path("reviews/<int:review_id>/delete/", review_views.delete_review, name="delete_review"),
]
