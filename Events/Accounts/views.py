from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from Accounts.models import Profile
from rest_framework.generics import CreateAPIView
from rest_framework import serializers, views, viewsets
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from EventAPP.models import Events
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter

# Create your views here.



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
   
class ProfileSerializer(serializers.ModelSerializer):
    """
    A student serializer to return the student details
    """
    user = UserSerializer(required=True)
    class Meta:
        model = Profile
        fields = ('user', 'age', 'gender', 'address')

    def create(self, validated_data):
      
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        s = Profile.objects.create(user=user,**validated_data)
        return s
    

class CreateNewUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"message":"User Registered Successfully"}
        return response
    

class LoginUser(views.APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username,password=password)
        login(request, user)
        u = User.objects.get(username = username)
        token = Token.objects.create(user = u)
        serializer = UserSerializer(user)
        return Response({"data":serializer.data, "Token":token.key,})
    
class LogoutUser(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({"data":"Logout Successful"})


class EventSerializer(ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'
    # event_status = serializers.SerializerMethodField
    # def get_event_status(self, status):
    #     if status.start_at > datetime.today:
    #         e_status = "Upcoming Event"
    #         return e_status
    #     else:
    #          e_status = "Past Event"
    #          return e_status
        
class EventRegister(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    def create(self, request, *args, **kwargs):
        response =  super().create(request, *args, **kwargs)
        response.data = {"message":"Event Created Successfully"}
        return response
    

class EventFilterSet(FilterSet):
    event_name = CharFilter(lookup_expr='contains')
    class Meta:
        model = Events
        fields = ['event_name']

class SearchEvents(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilterSet    



class ChangePASS(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        u = User.objects.get(username=request.user)
        u.set_password(request.data['password'])
        u.save()
        return Response({"data":"Password Changed Successfully"})    
    



from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print(reset_password_token)
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Reset Password"),
        # message:
        email_plaintext_message,
        # from:
        "punarsidhu909@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    # msg.attach_alternative(email_html_message, "text/html")
    msg.send()