from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('emailorphone', 'type', 'otp', 'otp_expiry')
    search_fields = ('emailorphone', 'type')
    list_filter = ('type',)
    ordering = ('emailorphone',)
    readonly_fields = ('otp_expiry',)  # Making otp_expiry read-only

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('name', 'emailorphone', 'place', 'state', 'date')
    search_fields = ('name', 'emailorphone', 'place', 'state')
    list_filter = ('state', 'date')
    ordering = ('-date',)

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'emailorphone', 'place', 'state', 'date')
    search_fields = ('name', 'emailorphone', 'place', 'state')
    list_filter = ('state', 'date')
    ordering = ('-date',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'subcategory_link', 'seller_link')
    search_fields = ('name', 'subcategory__name', 'seller__name')
    list_filter = ('subcategory', 'seller')
    ordering = ('name',)

    # Adding clickable links to related fields
    def subcategory_link(self, obj):
        url = reverse('admin:app_subcategory_change', args=[obj.subcategory.id])
        return format_html('<a href="{}">{}</a>', url, obj.subcategory.name)
    subcategory_link.short_description = 'Subcategory'

    def seller_link(self, obj):
        url = reverse('admin:app_seller_change', args=[obj.seller.id])
        return format_html('<a href="{}">{}</a>', url, obj.seller.name)
    seller_link.short_description = 'Seller'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'comment', 'pdate')
    search_fields = ('product__name', 'user__name')
    list_filter = ('rating', 'pdate')
    ordering = ('-pdate',)
    readonly_fields = ('product', 'user', 'rating', 'comment', 'pdate')  # All fields are read-only

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('checkout', 'product', 'quantity', 'price')
    search_fields = ('checkout__id', 'product__name')
    list_filter = ('checkout__date',)
    ordering = ('checkout__date',)
    readonly_fields = ('checkout', 'product', 'quantity', 'price')  # All fields are read-only

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('checkout', 'amount', 'date')
    search_fields = ('checkout__id',)
    list_filter = ('date',)
    ordering = ('-date',)
    readonly_fields = ('checkout', 'amount', 'date')  # All fields are read-only

@admin.register(DeliveryFeedback)
class DeliveryFeedbackAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'feedback', 'rating', 'date')
    search_fields = ('order__id', 'user__name')
    list_filter = ('rating', 'date')
    ordering = ('-date',)
    readonly_fields = ('order', 'user', 'feedback', 'rating', 'date')  # All fields are read-only

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'complaint', 'date')
    search_fields = ('user__name', 'order__id')
    list_filter = ('date',)
    ordering = ('-date',)
    readonly_fields = ('user', 'order', 'complaint', 'date')  # All fields are read-only

@admin.register(DeliveryBoy)
class DeliveryBoyAdmin(admin.ModelAdmin):
    list_display = ('name', 'emailorphone', 'photo', 'place', 'pincode', 'state', 'gender', 'date', 'id_proof')
    search_fields = ('name', 'emailorphone', 'place', 'state')
    list_filter = ('state', 'date')
    ordering = ('-date',)

@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('login','subject', 'message', 'date')
    search_fields = ('date', 'subject')
    list_filter = ('date',)
    ordering = ('-date',)
    readonly_fields = ('login', 'subject', 'message', 'date')  # All fields are read-only

