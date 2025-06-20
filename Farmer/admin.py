from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib import messages
from django.contrib.admin import AdminSite
from .models import Products, Crop, Contact, CropRecommendationLog, CropDataset, AddCropData, Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'comment', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'comment']
    readonly_fields = ['created_at']
import csv
import os

# Customize admin site
admin.site.site_header = 'Crop Recommendation System Administration'
admin.site.site_title = 'Crop Recommendation Admin Portal'
admin.site.index_title = 'Welcome to Crop Recommendation Portal'

class CropDatasetAdmin(admin.ModelAdmin):
    list_display = ['label', 'n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall']
    list_filter = ['label']
    search_fields = ['label']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Export all entries to CSV after saving
        self.export_to_csv()
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # Update CSV after deletion
        self.export_to_csv()
    
    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        # Update CSV after bulk deletion
        self.export_to_csv()
    
    def export_to_csv(self):
        with open('Agri/static/Crop_recommendation.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
            # Write data
            for entry in CropDataset.objects.all():
                writer.writerow([
                    entry.n, entry.p, entry.k, entry.temperature,
                    entry.humidity, entry.ph, entry.rainfall, entry.label
                ])

class CropRecommendationLogAdmin(admin.ModelAdmin):
    list_display = ['recommended_crop', 'n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall', 'created_at']
    list_filter = ['recommended_crop', 'created_at']
    search_fields = ['recommended_crop']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

class AddCropDataAdmin(admin.ModelAdmin):
    list_display = ['label', 'n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall', 'added_at']
    list_filter = ['label', 'added_at']
    search_fields = ['label']
    readonly_fields = ['added_at']

    def save_model(self, request, obj, form, change):
        # First, save the model instance
        super().save_model(request, obj, form, change)
        
        # Then, append the data to the CSV file
        csv_path = 'Agri/static/Crop_recommendation.csv'
        
        # Check if file exists and if it's empty
        file_exists = os.path.exists(csv_path)
        file_empty = file_exists and os.path.getsize(csv_path) == 0
        
        # Open file in append mode
        with open(csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            
            # Write header if file is new or empty
            if not file_exists or file_empty:
                writer.writerow(['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
            
            # Write the new data row
            writer.writerow([
                obj.n, obj.p, obj.k, obj.temperature,
                obj.humidity, obj.ph, obj.rainfall, obj.label
            ])
        
        messages.success(request, f"Data for {obj.label} has been added to the dataset successfully!")

# Register your models here.
admin.site.register(Products)
admin.site.register(Crop)
admin.site.register(Contact)
admin.site.register(CropRecommendationLog, CropRecommendationLogAdmin)
admin.site.register(CropDataset, CropDatasetAdmin)
admin.site.register(AddCropData, AddCropDataAdmin)
admin.site.register(Feedback, FeedbackAdmin)
