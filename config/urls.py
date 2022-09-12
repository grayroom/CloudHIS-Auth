from django.urls import path, re_path
from auths import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.views.generic.base import RedirectView

urlpatterns = [
    re_path(r'^auth/home/', views.HomeView.as_view(), name='home'),
    path('auth/', RedirectView.as_view(url='/auth/home/')),
    path('', RedirectView.as_view(url='auth/home/')),

    path('auth/api/login/', views.JWTLoginView.as_view(), name='login'),
    path('auth/api/signup/', views.JWTSignupView.as_view(), name='signup'),
    path('auth/api/info/', views.UserInformationView.as_view(), name='userinfo'),
    path('auth/api/logout/', views.logout_view, name='logout'),

    # NOTE: simple JWT 에서 제공하는 뷰
    path('auth/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
