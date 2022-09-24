from django.urls import path, re_path
from auths import views
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView, TokenVerifyView
from django.views.generic.base import RedirectView

urlpatterns = [
    # NOTE: user 관련
    path('auth/api/user/login/', views.JWTLoginView.as_view(),
         name='login'),
    path('auth/api/user/signup/', views.JWTSignupView.as_view(),
         name='signup'),
    path('auth/api/user/info/', views.UserInformationView.as_view(),
         name='userinfo'),
    path('auth/api/user/logout/', views.UserLogoutView.as_view(),
         name='logout'),

    # NOTE: token 생명주기 관련
    path('auth/api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('auth/api/token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),

    # NOTE: re_path를 통해 routing을 vue-router에게 인가
    re_path(r'^auth/', views.HomeView.as_view(), name='home'),
    path('', RedirectView.as_view(url='/auth/')),
]
