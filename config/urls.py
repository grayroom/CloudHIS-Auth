from django.urls import path
from auths import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('auth/home/', views.HomeView.as_view(), name='home'),
    path('', RedirectView.as_view(url='auth/home/')),

    path('api/user/login/', views.JWTLoginView.as_view(), name='login'),
    path('api/user/signup/', views.JWTSignupView.as_view(), name='signup'),
    path('api/user/info/', views.UserInformationView.as_view(), name='userinfo'),
    path('api/user/logout/', views.logout_view, name='logout'),

    # NOTE: simple JWT 에서 제공하는 뷰
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
