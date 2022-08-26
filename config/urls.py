"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topicss/http/urls/
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
from django.urls import path
from auths import views

urlpatterns = [
    path('login/', views.JWTLoginView.as_view(), name='login'),
    path('signup/', views.JWTSignupView.as_view(), name='logout'),

    # NOTE: 아래 URL 미구현... 구현필요
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('token/revoke/', TokenRevokeView.as_view(), name='token_revoke'),
    # path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
