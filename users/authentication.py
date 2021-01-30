import jwt
import datetime
from django.conf import settings
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication

def generate_access_token(user):
    payload ={
        'user_id':user.id,
        'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=100),
        'iat':datetime.datetime.utcnow()
    }
    return jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")

class JwtAuthentication(BaseAuthentication):

    def authenticate(self,request):
        token = request.COOKIES.get('jwt')
        if token is None:
            return None
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Unauthenticated user")
        try:
            user = get_user_model().objects.get(id=payload['user_id'])
        except AuthenticationFailed:
            raise AuthenticationFailed("user not found")
        return (user,None)
