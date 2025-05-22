from django.urls import path
from burhanimart import views
from django.contrib.auth import views as authentication
from .forms import LoginForm, OldPasswordChangeForm, ForgotPasswordSendMail, SetNewPassword
urlpatterns = [

    #Base urls
    path('',views.home, name='home'),
    #Slider url
    path('slider/<int:id>', views.slider),
    # Product Detail url
    path('product-detail/<int:id>/', views.productdetail, name='product-detail'),
    path('cloth-category/', views.cloth_category, name='cloth-category'),
    path('all-category/', views.all_category, name='all-category'),
    path('account-detail/',views.account_detail, name='account-detail'),


    # Cart url
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('view-cart-product/', views.view_cart_product, name='view-cart-product'),
    path('minus-cart-product/', views.minus_cart_product, name='minus-cart-product'),
    path('add-cart-product/', views.add_cart_product, name='add-cart-product'),
    path('remove-cart-product/', views.remove_cart_item, name='remove-cart-item'),
    # address urls
    path('add-new-address/', views.add_new_address, name='add-new-address'),
    path('save-address/', views.save_address, name='save-address'),
    path('<int:id>/', views.delete_save_address, name='delete-save-address'),
    path('update-address/<int:id>/', views.update_address, name='update-address'),

    path('checkout/', views.checkout, name='checkout'),
    path('order-placed-successfully/', views.order_placed_successfully, name='order-placed-successfully'),
    path('order-view/', views.order_view, name='order-view'),
    path('order-detail/<int:id>', views.order_detail, name='order-detail'),
    path('search-product/', views.search_product, name='search-product'),
    path('about-us/', views.about_us, name='about-us'),
    path('contact-us/', views.contact_us, name='contact-us'),

    # path('payment/', views.payment, name='payment'),







    # path('profile/', views.ProfileView.as_view(), name='address'),


    




    #authentication urls
    path('login/', authentication.LoginView.as_view(template_name='login.html', 
    authentication_form=LoginForm), name='login'),

    path('logout/', authentication.LogoutView.as_view(next_page='home'), name='logout'),

    path('signup/',views.signup, name='signup'),

    path('passwordchange/', authentication.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=OldPasswordChangeForm, success_url='/password-change-successfully/'), name='passwordchange'),

    path('password-change-successfully/', authentication.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    
    path("forgot-password/", authentication.PasswordResetView.as_view(template_name='password_reset.html', form_class=ForgotPasswordSendMail), name="password_reset"),

    path("reset-password-link-sent-successfully", authentication.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),

    path("password-reset-confirm/<uidb64>/<token>/", authentication.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=SetNewPassword), name="password_reset_confirm"),

    path("password-reset-complete/", authentication.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),    

   
]