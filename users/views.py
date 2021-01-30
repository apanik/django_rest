from .models import User,Permissons,Role
from django.shortcuts import render
from rest_framework import exceptions, viewsets,generics,mixins
from .serializers import UserSerializer,PermissonSerializer,RolesSerializer
from rest_framework.response import Response
from .authentication import JwtAuthentication
from .authentication import generate_access_token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,APIView
from src.pagination import CustomPaginator


# Create your views here.
@api_view(['POST'])
def register(request):
    data = request.data
    if data['password']!=data['confirm_password']:
        raise exeptions.APIExeptions("Password do not match")
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email = email)
    except:
        raise exceptions.AuthenticationFailed("User not found")
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("Password not match")
    response = Response()
    token  = generate_access_token(user)
    response.set_cookie(key="jwt",value=token,httponly=True)
    response.data = {
        'jwt' : token
    }
    return response

@api_view(['post'])
def logout(_):
    response = Response()
    response.delete_cookie(key="jwt")
    response.data = {
        'message' : 'successfully logged out'
    }
    return response


@api_view(['GET'])
def user(request):
    user = User.objects.all()
    serializer = UserSerializer(User.objects.all(),many=True)
    return Response(serializer.data)

class AuthenticatedUser(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get(slef,request):
        serializer = UserSerializer(request.user)
        return Response(
            {
                "data":serializer.data
                }
            )


class Permisson(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get(slef,request):
        serializer = PermissonSerializer(Permissons.objects.all(),many=True)
        return Response(
            {
                "data":serializer.data
                }
            )

class RolesSet(viewsets.ViewSet):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]
    
    def list(self,request):
        serializer = RolesSerializer(Role.objects.all(),many=True)
        return Response({
            'data':serializer.data
            })       
        
    def retrive(self,request,pk=None):
        role = Role.objects.get(id=pk)
        serializer = RolesSerializer(role)
        return Response({
            'data':serializer.data
        })
        
    def create(self,request):
        serializer = RolesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
                "data":serializer.data
            })
        
    def update(self,request,pk=None):
        role = Role.objects.get(id=pk)
        serializer = RolesSerializer(instance=role,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "data":serializer.data
        })
    def destroy(self,request,pk=None):
        role = Role.objects.get(id=pk)
        role.save()
        return Response({
            'status':'no content'
        })
    
    
    
class UserGenericView(generics.GenericAPIView,mixins.ListModelMixin,mixins.RetrieveModelMixin):
        authentication_classes = [JwtAuthentication]
        permission_classes = [IsAuthenticated]
        queryset = User.objects.all()
        serializer_class = UserSerializer
        pagination_class = CustomPaginator
        
        def get(self,request,pk=None):
            if pk:
                return Response({
                    'data': self.retrieve(request,pk).data})
                                
            return(self.list(request))
                            
