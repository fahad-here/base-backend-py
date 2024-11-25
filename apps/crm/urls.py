from django.urls import path, include

urlpatterns = [
    path('customers/', include('apps.crm.customers.urls')),
    path('operations/', include('apps.crm.operations.urls')),
    path('reports/', include('apps.crm.reports.urls')),
]
