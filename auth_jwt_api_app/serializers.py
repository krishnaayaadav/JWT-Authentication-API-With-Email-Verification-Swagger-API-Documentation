from rest_framework import serializers
from .models import User

class RegisterationSerializer(serializers.ModelSerializer):
   password2 = serializers.CharField(style={'input-type': 'password'},write_only=True, label='confirm password')
   class Meta:
      model  = User
      fields = ('name', 'email', 'password', 'password2',  'terms_condition')
      
      extra_kwargs = {
         'password': {'write_only': True}
      }
      
   def validate(self, attrs):
      
      if ('password' and 'password2') in attrs:
         password = attrs.get('password',None)
         password2 = attrs.get('password2',None)
         
         if password == password2:
            return attrs
         else:
            raise serializers.ValidationError("Password and confirm password doesn't match")
         
      raise serializers.ValidationError('Password or confirm password not found')
   
   def  create(self, validate_data):
      return User.objects.create_user(**validate_data)
      
class LoginSerializer(serializers.ModelSerializer):
   
   email = serializers.EmailField(max_length=255)
   class Meta:
      model  = User
      fields = ('email', 'password')

class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ('id', 'name', 'email', 'is_active', 'is_admin', 'created_at', 'updated_at')