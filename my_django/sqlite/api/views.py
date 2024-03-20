from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import PathChecker
from .serializers import PathSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .check_structure import is_folder_valid


class PathList(generics.ListCreateAPIView):
    queryset = PathChecker.objects.all()
    serializer_class = PathSerializer

    def delete(self, request, *args, **kwargs):
        PathChecker.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PathRetrieveUpdateDestory(generics.RetrieveUpdateDestroyAPIView):
    queryset = PathChecker.objects.all()
    serializer_class = PathSerializer
    lookup_field = "pk"



@api_view(['GET', 'PUT', 'DELETE'])
def path_detail(request, pk):
    try:    
        
        try:
            snippet = PathChecker.objects.get(pk=pk)
            print("Primary Key : ", pk)

        except PathChecker.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':

                print("GET REQUEST")
                serializer = PathSerializer(snippet)
                given_data = serializer.data
                given_path = given_data["path"] 
                print("Data : " , given_data)
            
                if is_folder_valid(given_path = given_path):
                    print("Valid Folder Structure")
                    return Response(serializer.data, status = status.HTTP_200_OK)

                else:
                    print("Invalid Folder Structure")
                    return Response(serializer.data, status = status.HTTP_406_NOT_ACCEPTABLE)



        elif request.method == 'PUT':
            print("PUT REQUEST")
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        elif request.method == 'DELETE':
            print("DELETE REQUEST")
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        elif request.method == 'POST':
            print("POST REQUEST")
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        elif request.method == 'PATCH':
            print("PATCH REQUEST")
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        elif request.method == 'HEAD':
            print("HEAD REQUEST")
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        elif request.method == 'OPTIONS':
            print("OPTIONS REQUEST")
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        pass
