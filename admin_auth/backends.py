from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailBackend(BaseBackend):
    """
    Authenticate using username and password.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        User = get_user_model()  # ✅ Moved inside the method

        try:
            user = User.objects.get(username=username)
            print('user', user)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        return getattr(user, 'is_active', False)

    def get_user(self, user_id):
        User = get_user_model()  # ✅ Also move it here
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
