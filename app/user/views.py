from rest_framework import generics
from user.serilizers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
