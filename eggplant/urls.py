from django.conf.urls import include, url

urlpatterns = [
    url(
        r'^invitations/',
        include('eggplant.invitations.urls', namespace='invitations')
    ),
    url(r'^profiles/', include('eggplant.profiles.urls', namespace='profiles')),
    url(
        r'^departments/',
        include('eggplant.departments.urls', namespace='departments',)
    ),
    url(r'^accounts/', include('eggplant.accounts.urls', namespace='accounts')),
    url(r'^market/', include('eggplant.market.urls', namespace='market')),
    url(r'^', include('eggplant.dashboard.urls', namespace='dashboard')),
]
