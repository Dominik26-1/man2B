"""man2b URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from feedback.views import *

router = routers.DefaultRouter()
router.register(r'company', CompanyView)

router.register(r'project', ProjectView)
router.register(r'team', TeamView)
router.register(r'department', DepartmentView)
router.register(r'skill', SkillView)
router.register(r'position', PositionView)
router.register(r'feedback', FeedbackView)
router.register(r'rating', RatingView)
router.register(r'employee', EmployeeView)
router.register(r'employee_management', EmployeeManagementView)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'debug', include(debug_toolbar.urls))

]
urlpatterns += router.urls
