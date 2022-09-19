from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="VIPPU API",
        default_version="v1",
        description="HRIMS Backend",
        # terms_of_service="https://www.homepetvet.com",
        contact=openapi.Contact(email="shredakajoshua@gmail.com"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), # Who can view the api 
)

urlpatterns = [
    re_path(
        r"^(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),  # <-- Here
    path(
        "", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"
    ),  # <-- Here
    path("", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("source/", include("api.urls")),
    path("accounts/", include("allauth.urls"), name="socialaccount_signup"),
]
