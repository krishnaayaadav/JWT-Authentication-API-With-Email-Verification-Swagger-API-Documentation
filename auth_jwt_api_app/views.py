from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.backends import TokenBackend


from .models import User
from .custom_renders import CustomRenderer
from .serializers import RegisterationSerializer, LoginSerializer, ProfileSerializer
from django.contrib.auth import authenticate


###### My Current Project ###

# generate token manually
def get_tokens_for_user(user):
   """get token for authenticated user"""
   refresh = RefreshToken.for_user(user)

   return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
   }

# get current user id from their access token
def get_current_user_from_token(token):
   """Get current user id using user access token instead of from request.user"""
   try:
      access_token = AccessToken(token)
   except :
      pass
      print('\n Exception while  getting user id')
   
   else:
      user_id = User.objects.get(pk = access_token['user_id']).id
      return user_id
      
class UserRegisterAPI(APIView):
   
   authentication_classes = [JWTAuthentication]
   permission_classes     = [AllowAny]
   renderer_classes        = [CustomRenderer]
   
   def post(self, request,  format=None):
      serializer = RegisterationSerializer(data = request.data)
      if serializer.is_valid(raise_exception=True):
         user = serializer.save()
         name = str(user.name).title()
         response ={
                     'detail': f'Congrats {name} your successfuly register',
                     'token': get_tokens_for_user(user)
                      
                     }
         return Response(response, status=status.HTTP_201_CREATED)
      else:
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
   
   renderer_classes = [CustomRenderer]
   
   def post(self, request,format=None, *args, **kwargs):
      serializer = LoginSerializer(data=request.data)
      
      if serializer.is_valid(raise_exception=True):
         email = serializer.validated_data.get('email')
         password = serializer.validated_data.get('password')
         
         try:
            auth = authenticate(email=email, password=password)
            
         except:
            response = {'errors': {'non_field_errors':'Email or Password in incorrect'}}
            res_status   = status.HTTP_404_NOT_FOUND
            
         else:
            if not auth: # if user is not authenticated than
               response = {'errors': {'non_field_errors':'Email or Password in incorrect'}}
               res_status   = status.HTTP_404_NOT_FOUND
            else:
               # if user credential successfuly authenticated than
               name = str(auth.name).capitalize()
               
               response ={
                     'detail': f'Congrats {name} your successfuly logged-in',
                     'token': get_tokens_for_user(auth)
                     }
               res_status   = status.HTTP_200_OK
         
         return Response(response, status=res_status)
          
      else:
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardAPIView(APIView):
   authentication_classes = [JWTAuthentication]
   permission_classes     = [IsAuthenticated]
   
   def get(self, request, format=None):
      
      # print('\n',  request.headers)
      token = str(request.headers.get('authorization')).split()[1]
      
      user_id = get_current_user_from_token(token=token)

      user_profile = User.objects.get(pk = user_id)
      serializer   = ProfileSerializer(user_profile)
      response = {'msg': 'Welcome to dashboard', 'data': serializer.data}
      
      return Response(response, status=status.HTTP_200_OK)
   
class ChangePasswordAPIView(APIView):
   
   authentication_classes = [JWTAuthentication]
   permission_classes     = [IsAuthenticated]
   
   def post(self, request, format=None):
      token = str(request.headers.get('authorization')).split(' ')[1]
      user_id   = get_current_user_from_token(token)
      
      ##### Current Working On to complete it ######
            # Thank You
      
      
      pass