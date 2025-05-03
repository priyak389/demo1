from django.shortcuts import render,HttpResponse

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from .models import Customer

class crudapi(APIView):
    def get(self,request):
        id=request.data.get('id',None)
        if id:
            try:
                customer=Customer.objects.get(id=id)
                customerdata=CustomerSerializer(customer)
                print(customerdata)
                return Response(customerdata.data,status=status.HTTP_200_OK)
            except:
                return Response({'msg':'Data is not available'},status=status.HTTP_404_NOT_FOUND)
        
        else:
       
            customer=Customer.objects.all()
            print(customer)
            customerdata=CustomerSerializer(customer,many=True)

            print(customerdata)
            return Response(customerdata.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        customerdetails=request.data 
        print(customerdetails)
        customerdata=CustomerSerializer(data=customerdetails)
        print(customerdata)
        if customerdata.is_valid():
            customerdata.save()
            return Response({'Msg':'Data is successfully inserted'},status=status.HTTP_200_OK)
        return Response({'msg':'Data is not available'},status=status.HTTP_404_NOT_FOUND)

    
    def patch(self,request):
        new_data=request.data 
        id=new_data.get('id',None)
        print(id)
        if id:
            try:
                customer_data=Customer.objects.get(id=id)
                print(customer_data)
                customer_data=CustomerSerializer(customer_data,new_data,partial=True)
                if customer_data.is_valid():
                    customer_data.save()
                    return Response({'Msg':'Data is successfully updated'},status=status.HTTP_200_OK)
            except:
                return Response({'Msg':'data is not available'},status=status.HTTP_404_NOT_FOUND)
        
        return Response({'msg':'update request'},status=status.HTTP_200_OK)
    
    def delete(self,request):
         id=request.data.get('id',None)
         if id:
            try:
                customer=customer.objects.get(id=id)
                customer.delete()
                 
                return Response({'msg':'Data is successfully deleted'},status=status.HTTP_200_OK)
            except:
                return Response({'msg':'Data is not available'},status=status.HTTP_404_NOT_FOUND)
        
           
         return Response({'Msg':'Please provide id'},status=status.HTTP_200_OK)