from django.urls import path

from . import views

urlpatterns = [
    path('api/auth/login/', views.AgentLoginView.as_view(), name='agent-login'),
    path('api/auth/token/', views.TokenObtainView.as_view(), name='token-obtain'),
    path('api/auth/token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    path('api/agents/execute/', views.AgentExecuteView.as_view(), name='agent-execute'),
    path('api/agents/trigger/', views.AgentTriggerView.as_view(), name='agent-trigger'),
    path('api/data/export/', views.DataExportView.as_view(), name='data-export'),
    path('api/data/upload/', views.DataUploadView.as_view(), name='data-upload'),
    path('api/agents/status/', views.AgentStatusView.as_view(), name='agent-status'),
    path('api/health/', views.HealthCheckView.as_view(), name='health-check'),
]
