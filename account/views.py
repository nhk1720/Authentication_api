from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import UserRegistrationSerializer,LoginSerializer,ProfileSerializer,ChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistationview(APIView):
    def post(self,request,format='None'):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successful'},status=status.HTTP_201_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self,request,format='None'):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Success'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
class UserProfileView(APIView):
 permission_classes = [IsAuthenticated]
 def get(self,request,format=None):   
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer=ChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordEmailView(APIView):
    def post(self,request):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password Reset link send. please check your email'},status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
     def post(self,request,uid,token,format=None):
         serializer=UserPasswordResetSerializer(data=request.data, context={'uid':uid,'token':token})
         if serializer.is_valid(raise_exception=True):
             return Response({'msg':'Password reset successfully'},status=status.HTTP_200_OK)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                                                
    
    
    
    
    
    
    
    
    

             
                

        
