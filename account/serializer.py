from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
       
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        return attrs
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=50)
    class Meta:
        model=User
        fields=["email","password"]  
         
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']
        
class ChangePasswordSerializer(serializers.Serializer):
    type=serializers.CharField(max_length=255)
    password=serializers.CharField(max_length=255,write_only=True)
    password2=serializers.CharField(max_length=255,write_only=True)
    
    class Meta:
        model=User
        fields=['password','password2','type']
        
    def validate(self, attrs):
        type = attrs.get("type")
        password=attrs.get('password')
        password2=attrs.get('password2')
        
        if type.upper() =="LOGIN":
            user=self.context.get('user')
            if password!=password2:
                raise serializers.ValidationError("password and confirm password doesn't match")
            user.set_password(password)
            user.save()
        else:
            raise serializers.ValidationError("you do not have type == login")

        return attrs
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    
    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('password rest token',token)
            link='http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('password rest link',link)
            #send reset mail
            return attrs
        else:
            raise ValidationError('YOU ARE NOT A REGISTER USER')
        
class UserPasswordResetSerializer(serializers.Serializer):
    type=serializers.CharField(max_length=255)
    password=serializers.CharField(max_length=255,write_only=True)
    password2=serializers.CharField(max_length=255,write_only=True)
    class Meta:
        model=User
        fields=['password','password2','type']
        
    def validate(self, attrs):
        try:
            type = attrs.get("type")
            password=attrs.get('password')
            password2=attrs.get('password2')
            
            if type.upper() =="LOGIN":
                uid=self.context.get('uid')
                token=self.context.get('token')

                if password!=password2:
                    raise serializers.ValidationError("password and confirm password doesn't match")
                id=smart_str(urlsafe_base64_decode(uid))
                user=User.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user,token):
                    raise ValidationError('Token is not valid or Expired')
                user.set_password(password)
                user.save()
            else:
                raise serializers.ValidationError("you do not have type == login")
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not valid or Expired')
        
            
        
        
        
    

