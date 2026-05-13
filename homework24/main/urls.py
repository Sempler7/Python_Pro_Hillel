
from django.contrib import admin
from django.urls import path

from task_manager.api import api as tasks_api
from shop.api import api as shop_api
from movies.api import api as movies_api
from blog.api import api as blog_api
from monitoring.api import api as monitoring_api
from library.api import api as library_api
from studentCourse.api import api as education_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/task_manager/', tasks_api.urls),
    path('api/shop/', shop_api.urls),
    path('api/movies/', movies_api.urls),
    path('api/blog/', blog_api.urls),
    path('api/monitoring/', monitoring_api.urls),
    path('api/library/', library_api.urls),
    path('api/studentCourse/', education_api.urls),
]
