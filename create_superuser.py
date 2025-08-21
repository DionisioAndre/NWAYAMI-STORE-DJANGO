import os
import django
from django.contrib.auth import get_user_model

# Configure o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loja.settings")
django.setup()

# Defina os detalhes do superusuário
User = get_user_model()
username = 'admin'
email = 'admin@gmail.com'
password = '1234'

# Tente obter o superusuário
try:
    user = User.objects.get(username=username)
    # Atualiza a senha se o usuário já existir
    user.set_password(password)
    user.save()
    print("Superusuário atualizado com sucesso!")
except User.DoesNotExist:
    # Criação do superusuário se não existir
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superusuário criado com sucesso!")
