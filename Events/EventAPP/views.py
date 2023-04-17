from django.shortcuts import render
from EventAPP.models import Events,Participants

from rest_framework.response import Response
from rest_framework import views
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class JoinEvent(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        event = Events.objects.get(id = pk)
        request.data['user'] = request.user.id
        Participants.objects.create(user = request.user, event_name = event)
        return Response({"data":"Successfully joined the event."})
    

class LeaveEvent(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request ,pk):
        event = Participants.objects.get(event_name_id = pk, user_id = request.user.id)
        event.has_joined = False
        event.save()
        return Response({"data":"You left the event."})    