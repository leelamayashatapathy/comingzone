from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from.models import Student,Book

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from .serializers import StudentSerializer,BookSerializer,UserSerializer,NewBookSerializer,CrteateBookSerializer,RegisterSerializer,LoginSerializer


# from rest_framework.mixins import ListModelMixin,CreateModelMixin
# from rest_framework.generics import GenericAPIView



class RegistrationView(APIView):
    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "msg":"User not created",
                "error": serializer.errors
            })
        serializer.save()
        response = {
        "status": True,
        "message": "User Created",
        "student" : serializer.data
        }
        return Response(response)
    
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                # Optionally: generate token here (e.g., JWT or DRF token)
                token, created = Token.objects.get_or_create(user=user)
                user_data = LoginSerializer(user).data
                
                return Response({
                    "status": True,
                    "message": "User logged in successfully",
                    "data": user_data,
                    "token": token.key
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "message": "Invalid credentials"
                }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "status": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
            
                    
            
            


















@api_view(['get'])
def index(request):
    
    students = ["Litu", "Ramesh", "Umesh", "Tinguru"]
    data = {
        "status": True,
        "message": "This is a response of rest framework",
        "students": students,
        
    }
    
    return Response(data)


@api_view(["POST","GET","PUT","DELETE"])
def get_data(request, id = None):
    # print(vars(request))
    if request.method == "POST":
         # with serializer
        
        data = request.data
        serializer = StudentSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "msg":"Stdent not created",
                "error": serializer.errors
            })
        serializer.save()
        response = {
        "status": True,
        "message": "Fetched all student data",
        "student" : serializer.data
        }
        return Response(response)
        
        # data = request.data
        # Student.objects.create(**data)
        # student = Student.objects.all().values()
        # response = {
        # "status": True,
        # "message": "Student data created",
        # "student" : list(student)
        # }
        # return Response(response)
        
    elif request.method == "GET":
       
        # student = Student.objects.all().values().order_by("name")
        # response = {
        # "status": True,
        # "message": "Fetched all student data",
        # "student" : list(student)
        # }
        # return Response(response)
        
        # without mentioning id in url
        
        if (_id := request.GET.get('id')):
            student = Student.objects.get(id=_id)
            result = StudentSerializer(student)
            response = {
            "status": True,
            "message": "Fetched all student data",
            "student" : result.data
            }
            return Response(response)
            
        
        # with serializer
        # quesryset = Student.objects.all()
        # result = StudentSerializer(quesryset,many=True)
        # response = {
        # "status": True,
        # "message": "Fetched all student data",
        # "student" : result.data
        # }
        # return Response(response)
        
    elif request.method == "PUT":
        data = request.data
        if id is not None:
            
            try:
                student_obj = Student.objects.get(id=id)
            except Student.DoesNotExist:
                return Response({"msg": "Student not found"}, status=404)

            serializer = StudentSerializer(student_obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {'status': 'updated', 'student': serializer.data}
                return Response(res)
            else:
                return Response({"error": serializer.errors}, status=400)
        else:
            return Response({"msg": "Student ID is required"}, status=400)

        
        
        # data = request.data
        # if id != None:
        #     student = Student.objects.get(id = id)
        #     student.name = data['name']
        #     student.dob = data ['dob']
        #     student.email = data['email']
        #     student.phone = data['phone']
        #     student.save()
        #     res = {'status': 'updated', 'student': {
        #             'id': student.id,
        #             'name': student.name,
        #             'email': student.email,
        #             'phone' : student.phone
        #         }}
        #     return Response (res)
        # else:
        #     return Response({"msg": "Student not found"})
        
    elif request.method == "DELETE":
        data = request.data
        if id != None:
            student = Student.objects.get(id = id)
            student.delete()
            return Response({"msg":"Student data has been deleted"})
        
        
        
        
class BookView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        query_set = Book.objects.all()
        serializer = NewBookSerializer(query_set,many=True)
        return Response ({
            "msg":"All data fetched",
            "data":serializer.data
        })
    def post(self,request):
        data = request.data
        # book = BookSerializer(data=data)
        book = NewBookSerializer(data=data)
        
        if not book.is_valid():
            return Response({
                "status": True,
                "message": "Error",
                "student" : book.errors
            })
            
        book_instance = book.save()
        return Response({
                "status": True,
                "message": "Books Created",
                "student" : BookSerializer(book_instance).data
            })
            
    def put(self, request):
        data = request.data
        if (_id := request.GET.get('id')):
            book_obj = Book.objects.get(id=_id)
            book_ser = BookSerializer(book_obj,data=data,partial=True)
            if not book_ser.is_valid():
                return Response({
                    "status": True,
                    "message": "Error",
                    "student" : book_ser.errors
                })
                
            book_instance = book_ser.save()
            return Response({
                    "status": True,
                    "message": "Books Created",
                    "student" : BookSerializer(book_instance).data
                })
    

    


class UserApi(APIView):
    def post(self,request):
        data = request.data
        try:
            serializer = UserSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    "status":False,
                    "msg":"Stdent not created",
                    "error": serializer.errors
                })
            # serializer.save()
            response = {
            "status": True,
            "message": "Fetched all student data",
            "student" : serializer.data
            }
            return Response(response)
        except Exception as e:
            return Response(e)