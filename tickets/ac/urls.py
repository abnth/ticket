from django.conf.urls  import patterns , include , url


urlpatterns = patterns( '',
             
     url(r'^$', 'ac.views.main', name='Main'),
     url(r'^display/(\d+)/$', "ac.views.display"),
     url(r'^search', "ac.views.display"),
     url(r'^submit_ticket',"ac.views.submit_ticket"),
     url(r'^register/$', "ac.views.register", name='register'),
     url(r'^login/$',"ac.views.user_login",name='login'),
     url(r'^logout/$',"ac.views.user_logout",name='logout'),

)