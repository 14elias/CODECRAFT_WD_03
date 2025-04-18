from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import status
from .serializers import UserSerializer
from .models import CustomUser

class Authenticated(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        return Response({'message':'authenticated'})
    
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        try:

            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            res = Response({
                'message':'loggedin successfully'
            },status=status.HTTP_200_OK)

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',  
            )

            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',  
            )
            return res
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            if not refresh_token:
                return Response({'error': 'No refresh token in cookies'}, status=status.HTTP_400_BAD_REQUEST)

            request.data._mutable = True
            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)
            access_token = response.data.get('access')

            res = Response({'message':'refreshed successfully'},status=status.HTTP_200_OK)

            res.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    path='/',  
                )
            res.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    path='/',  
                )
            return res
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class Logout(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        res = Response(
            {'message':'logged out successfully'},status=status.HTTP_200_OK
        )

        if access_token:
            res.delete_cookie(key='access_token', path='/')
        if refresh_token:
            res.delete_cookie(key='refresh_token', path='/')
        return res

class UserView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def get(self,request):
        user = CustomUser.objects.all()
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    def get(self,request,**kwargs):
        user = get_object_or_404(CustomUser,id=self.kwargs['pk'])
        serializer = UserSerializer(user)
        return Response(serializer.data)
    def delete(self,request,*args,**kwargs):
        user = get_object_or_404(CustomUser,id=self.kwargs['pk'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def patch(self,request,*args,**kwargs):
        user = get_object_or_404(CustomUser,id=self.kwargs['pk'])
        serializer = UserSerializer(user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)