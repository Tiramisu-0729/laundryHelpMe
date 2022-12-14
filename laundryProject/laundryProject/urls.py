from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('helpapp/', include('helpapp.urls')),  #URLにhelpapp/って指定されたら includeを呼び出す
    path('admin/', admin.site.urls),    #admin入るため
    path('', RedirectView.as_view(url='/helpapp/')), #URLに何も入れないとhelpapp/になる
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#画像読むのに必要