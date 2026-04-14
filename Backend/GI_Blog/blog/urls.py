from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    delete_post,
    UserPostListView,
    CategorieCreateView,
    ContactView,
    CatListView,
    TrendingView,
    LikeView,
    Read_laterView,
    ReadListView,
    SearchView,
    CommentView,
    Like2View,
    CommentUpdateView,

    delete_comment,
    add_comment
)


urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('trending/', TrendingView.as_view(), name='trending'),
    path('search/', SearchView, name='search'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user_posts'),
    path('read_later/<str:username>/posts/', ReadListView.as_view(), name='read_list'),
    path('categorie/<str:cat>/posts', CatListView.as_view(), name='cat_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/comment', CommentView.as_view(), name='comt_create'),
    path('comment/<int:pk>/update/<int:nb>/', CommentUpdateView.as_view(), name='comt_update'),
    path('post/<int:pk>/comment/<int:nb>', delete_comment, name='comt_delete'),
    path('categorie/new/', CategorieCreateView.as_view(), name='cat_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', delete_post, name='post_delete'),
    path('about/', views.about, name='about'),
    path('like/<int:pk>', LikeView, name="like_post"),
    path('like/post/<int:pk>', Like2View, name="like2_post"),
    path('read_later/<int:pk>', Read_laterView, name="read_post"),
    path('contact/', ContactView.as_view(), name='contact'),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),
]
