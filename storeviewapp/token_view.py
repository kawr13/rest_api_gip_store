from django.shortcuts import render
from django.views import View
from rest_framework.authtoken.models import Token
from storeviewapp.models import TokenUser


class AddToken(View):
    def get(self, request):
        context = {
            'title': 'Add token',
        }
        return render(request, 'storeviewapp/add_token.html', context)

    def post(self, request):
        user = request.user
        token, created = Token.objects.get_or_create(user=user)
        context = {
            'title': 'Add token',
            'token': token.key
        }
        return render(request, 'storeviewapp/add_token.html', context)
