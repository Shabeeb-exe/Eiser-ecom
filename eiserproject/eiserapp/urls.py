from django.urls import path
from eiserapp import views

urlpatterns = [
    #CUSTOMER:
    path('login/', views.login, name="login"),
    path('login_post/', views.login_post, name="login_post"),
    path('signup/', views.signup, name="signup"),
    path('signup_post/', views.signup_post, name="signup_post"),
    path('index/', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
    path('contact_post/<id>/', views.contact_post, name="contact_post"),
    path('blog/', views.blog, name="blog"),
    path('single_blog/', views.single_blog, name="single_blog"),
    path('elements/', views.elements, name="elements"),

    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('forgot_password_post/', views.forgot_password_post, name="forgot_password_post"),
    path('verify_otp/', views.verify_otp, name="verify_otp"),
    path('verify_otp_post/', views.verify_otp_post, name="verify_otp_post"),
    path('resend_otp/', views.resend_otp, name="resend_otp"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('reset_password_post/', views.reset_password_post, name="reset_password_post"),

    path('profile/', views.profile, name="profile"),
    path('profile_edit/<id>/', views.profile_edit, name="profile_edit"),
    path('change_password_post/',views.change_password_post, name="change_password_post"),

    # SELLER:
    path('seller_reg/', views.seller_reg, name="seller_reg"),
    path('seller_reg_post/', views.seller_reg_post, name="seller_reg_post"),
    path('seller_dashboard/', views.seller_dashboard, name="seller_dashboard"),

    path('contact_for_seller/', views.contact_for_seller, name="contact_for_seller"),

    path('seller_profile/', views.seller_profile, name="seller_profile"),
    path('seller_profile_edit/<id>/', views.seller_profile_edit, name="seller_profile_edit"),
    path('seller_change_password_post/',views.seller_change_password_post, name="seller_change_password_post"),

    #product mgmt:
    path('add_product/', views.add_product, name="add_product"),
    path('add_product_post/', views.add_product_post, name="add_product_post"),
    path('view_products/', views.view_products, name="view_products"),
    path('edit_product/<id>/', views.edit_product, name="edit_product"),
    path('edit_product_post/', views.edit_product_post, name="edit_product_post"),
    path('delete_product/<id>/', views.delete_product, name="delete_product"),

    #offer mgmt:
    path('view_offers/', views.view_offers, name="view_offers"),
    path('add_offer/', views.add_offer, name="add_offer"),
    path('add_offer_post/', views.add_offer_post, name="add_offer_post"),
    path('edit_offer/<id>/', views.edit_offer, name="edit_offer"),
    path('edit_offer_post/', views.edit_offer_post, name="edit_offer_post"),
    path('remove_offer/<id>/', views.remove_offer, name="remove_offer"),

    #customer product mgmt:
    path('shop/', views.shop, name="shop"),
    path('filter_products/', views.filter_products, name="filter_products"),
    path('category/<int:id>/', views.category, name="category"),
    path('filter_category_products/<int:category_id>/', views.filter_category_products, name="filter_category_products"),
    path('subcategory/<int:subcategory_id>/', views.subcategory, name='subcategory'),
    path('filter_subcategory_products/<int:subcategory_id>/', views.filter_subcategory_products, name='filter_subcategory_products'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('search/', views.search, name="search"),
    path('delete_search_history/<int:history_id>/', views.DeleteSearchHistory.as_view(), name='delete_search_history'),
    path('clear_all_search_history/', views.ClearAllSearchHistory.as_view(), name='clear_all_search_history'),
    path('single_product/<p_id>/', views.single_product, name="single_product"),
    path('add_to_wishlist/', views.add_to_wishlist, name="add_to_wishlist"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('remove_wishlist_item/<id>/', views.remove_wishlist_item, name="remove_wishlist_item"),
    path('review_post/<p_id>/', views.review_post, name="review_post"),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart, name="cart"),
    path('update_quantity/<id>/', views.update_quantity, name="update_quantity"),
    path('remove_item/<id>/', views.remove_item, name="remove_item"),
    path('apply_coupon/', views.apply_coupon, name="apply_coupon"),
    path('cart_post/', views.cart_post, name="cart_post"),
    path('checkout/', views.checkout, name="checkout"),
    path('checkout_post/', views.checkout_post, name="checkout_post"),
    path('payment/<check_id>/', views.payment, name="payment"),
    path('payment_post/', views.payment_post, name="payment_post"),
    path('orders_history/', views.orders_history, name='orders_history'),
    path('order_details/<id>/', views.order_details, name='order_details'),
    path('cancel_order/<id>/', views.cancel_order, name='cancel_order'),
    path('tracking/<id>/', views.tracking, name="tracking"),
    path('return_item/<id>/', views.return_item, name='return_item'),

    #Seller order mgmt:
    path('view_orders/', views.view_orders, name="view_orders"),
    path('view_order_details/<id>/', views.view_order_details, name="view_order_details"),
    path('order_status/<int:id>/<str:action>/', views.order_status, name='order_status'),
    path('view_returns/', views.view_returns, name="view_returns"),
    path('item_returned/<int:id>/<str:action>/', views.item_returned, name="item_returned"),
    path('delivery_feedback/<id>/', views.delivery_feedback, name="delivery_feedback"),
    
    path('inventory/', views.inventory, name="inventory"),
    path('inventory_post/<id>/', views.inventory_post, name="inventory_post"),
    path('submit_complaint/', views.submit_complaint, name="submit_complaint"),
    path('view_complaints/', views.view_complaints, name="view_complaints"),

    #DELIVERY BOY:

    path('deliveryboy_reg/', views.deliveryboy_reg, name="deliveryboy_reg"),
    path('deliveryboy_reg_post/', views.deliveryboy_reg_post, name="deliveryboy_reg_post"),
    path('deliveryboy_home/', views.deliveryboy_home, name="deliveryboy_home"),
    path('dboy_profile/', views.dboy_profile, name="dboy_profile"),
    path('dboy_profile_edit/<id>/', views.dboy_profile_edit, name="dboy_profile_edit"),
    path('dboy_change_password_post/',views.dboy_change_password_post, name="dboy_change_password_post"),
    path('view_deliveryboy_orders/', views.view_deliveryboy_orders, name="view_deliveryboy_orders"),
    path('cod_payment_received/<id>/', views.cod_payment_received, name="cod_payment_received"),
    path('view_deliveryboy_order_details/<id>/', views.view_deliveryboy_order_details, name="view_deliveryboy_order_details"),
    path('view_delivery_boy_returns/', views.view_delivery_boy_returns, name="view_delivery_boy_returns"),
    path('view_delivery_feedbacks/', views.view_delivery_feedbacks, name="view_delivery_feedbacks"),
    path('contact_for_dboy/', views.contact_for_dboy, name="contact_for_dboy"),
]
