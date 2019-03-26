from rest_framework import generics

from users.serializers import UsersSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UsersSerializer