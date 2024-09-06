from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class Email_authenticate(ModelBackend):
   def authenticate(self, username=None, password = None,  **kwargs):
      UseModel = get_user_model()
      try:
        user = UseModel.objects.get(email=username)
      except UseModel.DoesNotExist:
         return None
      else:
         if user.check_password(password):
            return user
      return None
    
    