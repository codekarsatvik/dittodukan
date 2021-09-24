from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
    path('', views.home),
    path('product-detail/<int:pid>', views.product_detail, name='product-detail'),
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/<int:pid>', views.add_to_cart, name='add-to-cart'),
    path('pluscart/', views.pluscart, name='pluscart'),
    path('minuscart/', views.minuscart, name='minuscart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('delete/<int:itemid>', views.delete_from_cart, name='delete-from-cart'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('checklogin/', views.checklogin, name='checklogin'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),

    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    path('tshirt/', views.tshirts, name='tshirts'),
    path('tshirt/<slug:data>', views.tshirts, name='tshirtsdata'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/<int:data>', views.checkout, name='checkout'),
    path('checkoutdone/', views.checkoutdone, name='checkoutdone'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout')
   
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
