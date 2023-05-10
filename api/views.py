from rest_framework import permissions
from rest_framework import views, status, generics
from rest_framework.response import Response
from django.contrib.auth import login, logout
from . import serializers

class RegisterUserView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.data)
            login(request, user)
            return Response({'success': f'User signed up successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': f'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
    
class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user