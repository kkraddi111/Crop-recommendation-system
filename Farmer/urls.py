from django.urls import path 
from .import views 

urlpatterns = [
    path('index',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('service',views.service,name='service'),
    path('register',views.register,name='reg'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('product',views.product,name='product'),
    path('crop',views.crop,name='croprecommendation'),
    path('predict',views.predict,name='predict'),
    path('profile',views.profile,name='profile'),
    path('history',views.history,name='history'),
    path('delete-log/<int:log_id>',views.delete_log,name='delete_log'),
    path('add-data',views.add_data,name='add_data'),
    path('edit-data/<int:entry_id>',views.edit_data,name='edit_data'),
    path('delete-data/<int:entry_id>',views.delete_data,name='delete_data'),
    path('feedback',views.feedback,name='feedback'),
    path('edit-feedback/<int:feedback_id>',views.edit_feedback,name='edit_feedback'),
    path('delete-feedback/<int:feedback_id>',views.delete_feedback,name='delete_feedback'),
]
