from unicodedata import name
from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
   path("index/", views.index, name="index"),
   path('detail/<bpk>', views.detail, name="detail"),
   path('delete/<bpk>',views.delete_con, name="delete"),
   path('create/', views.create, name="create"),
   path('update/<bpk>', views.update, name="update"),
   path('creply/<bpk>', views.creply, name="creply"),
   path('board:delete_reply/<ipk><bpk>', views.delete_reply, name="delete_reply"),
   path('trans/', views.trans, name="TRANS"),
   path('likey/<bpk>', views.likey, name="likey"),
   path('bad/<bpk>', views.bad, name="bad"),
]
