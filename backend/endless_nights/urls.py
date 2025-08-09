"""
URL configuration for The Endless Nights Engine.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI

# Initialize the API - where witnesses report
api = NinjaAPI(
    title="Endless Nights API",
    version="0.1.0",
    description="Where knowledge has weight and nights never end"
)

# Import API routers
from worlds.api import router as worlds_router
from game.api import router as game_router
from parser.api import router as parser_router
from llm.api import router as llm_router
from worlds.db_inspector import router as inspector_router

# Add routers
api.add_router("/worlds/", worlds_router)
api.add_router("/game/", game_router)
api.add_router("/parser/", parser_router)
api.add_router("/llm/", llm_router)
api.add_router("/inspector/", inspector_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)