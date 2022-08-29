from django.urls import path
from auths import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('login/', views.JWTLoginView.as_view(), name='login'),
    path('signup/', views.JWTSignupView.as_view(), name='logout'),

    # NOTE: simple JWT 에서 제공하는 뷰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
