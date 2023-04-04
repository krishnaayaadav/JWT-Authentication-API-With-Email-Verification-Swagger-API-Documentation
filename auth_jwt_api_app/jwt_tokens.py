from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CutomToken(TokenObtainPairSerializer):
   
   @classmethod
   def get_token(cls, user):
      token = super().get_token(user)
      
      token['name'] = user.name
      
      return token