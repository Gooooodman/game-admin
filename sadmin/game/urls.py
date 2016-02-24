from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('game.views',

#yunwei
   # url(r'^data/$', 'game.game_data', name='game_data'),
    url(r'^install/$', 'game.game_install', name='game_install'),
    url(r'^log/$', 'game.game_read_log_file', name='game_read_log'),
    url(r'^clean/$','game.game_clean_log',name="game_clean_log"),
)

