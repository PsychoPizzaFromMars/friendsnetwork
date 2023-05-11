from rest_framework import permissions
from rest_framework import views, status, generics
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.db import IntegrityError
from .models import *
from . import serializers


class RegisterUserView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.data)
            login(request, user)
            return Response(
                {"success": f"User signed up successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.LoginSerializer(
            data=self.request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
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


class FriendsListView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        friends = request.user.friends
        serializer = serializers.UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FriendshipsListView(views.APIView):
    permission_classes = {permissions.IsAuthenticatedOrReadOnly}

    def get(self, request):
        user = request.user
        outgoing_requests = Friendship.objects.filter(from_user=user)
        incoming_requests = Friendship.objects.filter(to_user=user)
        serializer_outgoing_requests = serializers.FriendshipSerializer(
            outgoing_requests, many=True
        )
        serializer_incoming_requests = serializers.FriendshipSerializer(
            incoming_requests, many=True
        )

        return Response(
            {
                "outgoing_requests": serializer_outgoing_requests.data,
                "incoming_requests": serializer_incoming_requests.data,
            },
            status=status.HTTP_200_OK,
        )


class FriendshipView(views.APIView):
    permission_classes = {permissions.IsAuthenticated}

    def get(self, request, to_user_id):
        from_user = request.user
        to_user = User.objects.get(id=to_user_id)
        if from_user.friends.all().filter(id=to_user.id).exists():
            friendship_status = (
                f"You ({from_user.username}) and {to_user.username} are friends"
            )
            return Response({"status": friendship_status}, status=status.HTTP_200_OK)

        # Checking friendship status between two users
        outgoing_request_exists = Friendship.objects.filter(
            from_user=from_user, to_user=to_user
        ).exists()
        incoming_request_exists = Friendship.objects.filter(
            from_user=to_user, to_user=from_user
        ).exists()
        if outgoing_request_exists:
            friendship_status = (
                f"Pending outcoming friend request to {to_user.username}"
            )
            return Response({"status": friendship_status}, status=status.HTTP_200_OK)
        elif incoming_request_exists:
            friendship_status = (
                f"Pending incoming friend request from {to_user.username}"
            )
            return Response({"status": friendship_status}, status=status.HTTP_200_OK)
        else:
            friendship_status = f"You are in no relationship with {to_user.username}"
            return Response({"status": friendship_status}, status=status.HTTP_200_OK)

    # Accept or send request
    def post(self, request, to_user_id):
        from_user = request.user
        to_user = User.objects.get(id=to_user_id)
        try:
            if Friendship.objects.filter(from_user=to_user, to_user=from_user).exists():
                Friendship.objects.get(from_user=to_user, to_user=from_user).delete()
                from_user.friends.add(to_user)
                to_user.friends.add(from_user)
                return Response(
                    {"message": "Friend request accepted"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                friend_request = Friendship(from_user=from_user, to_user=to_user)
                friend_request.save()
                return Response(
                    {"message": "Friend request sent"}, status=status.HTTP_201_CREATED
                )
        except IntegrityError as e:
            return Response(
                {"message": e.args[0]}, status=status.HTTP_406_NOT_ACCEPTABLE
            )

    # Delete friend, delete outgoing request or decline incoming request
    def delete(self, request, to_user_id):
        from_user = request.user
        to_user = User.objects.get(id=to_user_id)
        if User.objects.filter(pk=from_user.id, friends=to_user).exists():
            from_user.friends.remove(to_user)
            to_user.friends.remove(from_user)
            return Response(
                {
                    "message": f"User {to_user.username} has been deleted from your friendlist "
                },
                status=status.HTTP_200_OK,
            )
        elif Friendship.objects.filter(from_user=from_user, to_user=to_user).exists():
            friend_request = Friendship.objects.get(
                from_user=from_user, to_user=to_user
            )
            friend_request.delete()
            return Response(
                {"message": f"Friend request to user {from_user.username} is deleted"},
                status=status.HTTP_200_OK,
            )
        elif Friendship.objects.filter(from_user=to_user, to_user=from_user).exists():
            friend_request = Friendship.objects.get(
                from_user=to_user, to_user=from_user
            )
            friend_request.delete()
            return Response(
                {
                    "message": f"Friend request from user {from_user.username} is declined"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": f"Relationship with user {from_user.username} doesn't exist"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
