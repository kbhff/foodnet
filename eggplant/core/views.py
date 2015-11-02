from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    """
    TODO: This mixin should be replaced with
    django.contrib.auth.mixin.LoginRequiredMixin in django 1.9
    """
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)
