from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class User1(AbstractUser):
    email = models.EmailField(unique=True)
    telefone = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        validators=[RegexValidator(regex='^\d{9}$', message='O telefone deve ter 9 dígitos.')]
    )
    eComprador = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

<<<<<<< HEAD
class Fatura(models.Model):
    numero = models.CharField(max_length=50)
    cliente_nome = models.CharField(max_length=100)
    cliente_email = models.EmailField()
    cliente_endereco = models.CharField(max_length=255)  # ← adicionar
    cliente_nif = models.CharField(max_length=20)        # ← adicionar
    valor_total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    data_emissao = models.DateField(auto_now_add=True)
    data_vencimento = models.DateField(null=True, blank=True)  # ← adicionar

    def __str__(self):
        return f"Fatura {self.numero} - {self.cliente_nome}"



class ProdutoFatura(models.Model):
    fatura = models.ForeignKey('Fatura', on_delete=models.CASCADE, related_name='produtos')
    codigo = models.CharField(max_length=50)
    descricao = models.TextField()
    quantidade = models.IntegerField()
    unidade = models.CharField(max_length=10, default='UND')
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def subtotal(self):
        return self.quantidade * self.preco_unitario * (1 - self.desconto / 100)

=======
>>>>>>> da0259fcee8726afb712a5afe2ca0ec21dfc0994
class Profile(models.Model):
    user = models.OneToOneField(User1, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    bio = models.CharField(max_length=300, blank=True)
    image = models.ImageField(default="user_images/default.jpg", upload_to="user_images")
    role = models.CharField(max_length=50, default='user')

    def __str__(self):
        return self.full_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User1, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price_non_negative'), 
        ]

    def __str__(self):
        return self.name

class Order(models.Model):
    buyer = models.ForeignKey(User1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    prestacao = models.PositiveIntegerField()  # Se necessário, considere uma validação adicional
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/buyer/', null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Order {self.id} by {self.buyer.username}'

    def clean(self):
        if self.prestacao <= 0:
            raise ValidationError('A prestação deve ser maior que zero.')

    def save(self, *args, **kwargs):
        # Garantir que a validação personalizada seja chamada ao salvar
        self.full_clean()
        super().save(*args, **kwargs)
