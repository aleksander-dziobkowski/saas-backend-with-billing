from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_kwargs = {
            "password":{'write_only':True}
        }
    
    def save(self):
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')
        
        if not password == password2:
            raise serializers.ValidationError({'error':'Passwords should be the same'})
        
        if User.objects.filter(email=self.validated_data.get('email')).exists():
            raise serializers.ValidationError({'error':'User with this email already exists'})
        
        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account