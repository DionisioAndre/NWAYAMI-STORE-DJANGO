from django.core.validators import RegexValidator  # Adicione esta linha
from rest_framework_simplejwt.tokens import Token
from lojaApp.models import User1, Profile, Product, Order
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User1
        fields = ['id', 'username', 'email', 'telefone']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adicionando informações do usuário ao token
        token['username'] = user.username
        token['email'] = user.email
        token['telefone'] = user.telefone
        token['eComprador'] = user.eComprador
        token['id'] = user.id
        
        # Adicionando campos de admin
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff

        if hasattr(user, 'profile'):
            token['full_name'] = user.profile.full_name
            token['bio'] = user.profile.bio
            token['image'] = str(user.profile.image)
            token['role'] = user.profile.role

        return token

telefone_validator = RegexValidator(
    regex=r'^\d{9}$',  # Adicione o 'r' antes da string
    message='O telefone deve ter 9 dígitos.'
)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    telefone = serializers.CharField(max_length=9, required=True, validators=[telefone_validator])
    eComprador = serializers.BooleanField(default=True)

    class Meta:
        model = User1
        fields = ['id', 'email', 'username', 'password', 'password2', 'telefone', 'eComprador']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "As senhas não coincidem. Por favor, tente novamente."})

        if User1.objects.filter(email=attrs['email']).exists():
            raise ValidationError({"email": "Este e-mail já está em uso. Por favor, escolha outro."})

        if User1.objects.filter(username=attrs['username']).exists():
            raise ValidationError({"username": "Este nome de usuário já está em uso. Por favor, escolha outro."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remover password2 antes de criar o usuário
        user = User1(**validated_data)  # Criação do usuário
        user.set_password(validated_data['password'])  # Define a senha de forma segura
        user.save()

        # Criação do perfil associado ao usuário
        Profile.objects.create(user=user)

        # Logging da criação do usuário
        logger.info(f'Usuário criado: {user.username}')

        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User1
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User1.objects.create_superuser(**validated_data)
        return user