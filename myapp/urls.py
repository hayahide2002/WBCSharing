from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),  # ルートパスに home をマップ
    path('group/create/', views.create_group, name='create_group'),  # グループ作成ページ
    path('group/join/', views.join_group, name='join_group'),  # グループ参加ページ
    path('group/<int:group_id>/select/', views.select_cards, name='select_cards'),
    path('group/<int:group_id>/selections/', views.view_selections, name='view_selections'),
    
]

