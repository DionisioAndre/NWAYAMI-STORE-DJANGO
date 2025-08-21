
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User1, Product, Order
from .serializers import RegisterSerializer,MyTokenObtainPairSerializer, ProductSerializer, OrderSerializer, UserSerializer,SuperUserSerializer
import logging


<<<<<<< HEAD
# minhaapp/views.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from .models import Fatura
from io import BytesIO
import os
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from .models import Fatura
from io import BytesIO
import os
from django.conf import settings

from django.http import HttpResponse, Http404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os
from django.conf import settings
from .models import Fatura  # ajuste conforme seu app
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import datetime, timedelta
from .models import Fatura, ProdutoFatura

@csrf_exempt
def criar_fatura(request):
    if request.method == 'POST':
        dados = json.loads(request.body)

        # Gerar número sequencial da fatura (exemplo simples)
        ultimo = Fatura.objects.order_by('-numero').first()
        if ultimo and ultimo.numero.isdigit():
            novo_numero = str(int(ultimo.numero) + 1).zfill(6)  # ex: 000001, 000002
        else:
            novo_numero = "000001"

        data_emissao = datetime.now().date()
        data_vencimento = data_emissao + timedelta(days=7)

        fatura = Fatura.objects.create(
            numero=novo_numero,
            data_emissao=data_emissao,
            data_vencimento=data_vencimento,
            cliente_nome=dados.get('cliente_nome'),
            cliente_endereco=dados.get('cliente_endereco'),
            cliente_nif=dados.get('cliente_nif'),
        )

        for p in dados.get('produtos', []):
            ProdutoFatura.objects.create(
                fatura=fatura,
                codigo=p['codigo'],
                descricao=p['descricao'],
                quantidade=p['quantidade'],
                unidade=p['unidade'],
                preco_unitario=p['preco_unitario'],
                desconto=p['desconto'],
            )

        return JsonResponse({'id': fatura.id, 'numero': fatura.numero}, status=201)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registrar Arial normal e negrito (no Windows)
try:
    pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', r'C:\Windows\Fonts\arialbd.ttf'))
except:
    # fallback se não encontrar Arial, usa Helvetica
    pass

# Definição das posições no template (em pontos PDF)
POSICOES = {
    "numero": (478, 579),
    "numero_vr": (178, 630),
    "data_emissao": (20, 576),
    "data_vencimento": (150, 576),
    "cliente_nome": (384, 710),
    "cliente_endereco": (384, 700),
    "cliente_nif": (325, 576),

    # Tabela de produtos (coordenadas de cada coluna) → nova ordem
    "col_codigo": 10,       # Código
    "col_descricao": 130,   # Descrição
    "col_preco": 365,       # Preço Unitário
    "col_unid": 430,        # Unidade
    "col_qtd": 455,         # Quantidade
    "col_desc": 499,        # Taxa / Desconto
    "col_subtotal": 560,    # Total

    # Pagamento
    "pagamento": (80, 120),
    "banco": (80, 105),
    "iban": (114, 290),

    # Total final
    "total": (530, 156),
    "total_s": (525, 230),
    "total_p": (258, 346),
    "total_p1": (178, 400),
}


# Função auxiliar para quebra de linha
def draw_wrapped_text(p, x, y, text, max_width, line_height=12, font="Arial", font_size=8):
    """
    Imprime texto quebrando em várias linhas se ultrapassar max_width
    """
    p.setFont(font, font_size)
    words = text.split(" ")
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if p.stringWidth(test_line, font, font_size) <= max_width:
            line = test_line
        else:
            p.drawString(x, y, line)
            y -= line_height
            line = word
    if line:
        p.drawString(x, y, line)
    return y


def gerar_proforma_pdf(request, fatura_id):
    try:
        fatura = Fatura.objects.get(id=fatura_id)
    except Fatura.DoesNotExist:
        raise Http404("Fatura não encontrada.")

    produtos = fatura.produtos.all()

    # Dados fixos da empresa
    FORMA_PAGAMENTO = "Transferência Bancária"
    BANCO = "BANCO BIC"
    IBAN = "0051 0000 3026 9840 1517 8"

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    caminho_imagem = os.path.join(settings.BASE_DIR, 'lojaApp', 'static', 'imagens', 'modelo_proforma.png')
    p.drawImage(caminho_imagem, 0, 0, width=A4[0], height=A4[1])
    p.setFont("Arial", 8)

    # Cabeçalho
    prefixo = "05NW"
    ano = fatura.data_emissao.strftime("%Y")
    numero_formatado = f"{prefixo}{ano}/{fatura.numero}"

    p.drawString(*POSICOES["numero"], numero_formatado)
    p.setFont("Arial", 11)
    p.drawString(*POSICOES["numero_vr"], numero_formatado)
    p.drawString(*POSICOES["data_emissao"], f"{fatura.data_emissao.strftime('%d/%m/%Y')}")
    p.drawString(*POSICOES["data_vencimento"], f"{fatura.data_vencimento.strftime('%d/%m/%Y')}")

    # Nome (Arial-Bold 8) e Endereço (Arial 8) com quebra automática
    draw_wrapped_text(
        p, POSICOES["cliente_nome"][0], POSICOES["cliente_nome"][1],
        f"{fatura.cliente_nome}", max_width=200, line_height=10,
        font="Arial-Bold", font_size=8
    )

    draw_wrapped_text(
        p, POSICOES["cliente_endereco"][0], POSICOES["cliente_endereco"][1],
        f"{fatura.cliente_endereco}", max_width=200, line_height=10,
        font="Arial", font_size=8
    )

    # NIF
    p.drawString(*POSICOES["cliente_nif"], f"{fatura.cliente_nif}")

    # Tabela de produtos
    y = 500
    total_geral = 0
    p.setFont("Arial", 8)

    for produto in produtos:
        subtotal = produto.quantidade * produto.preco_unitario * (1 - produto.desconto / 100)
        total_geral += subtotal

        if y < 150:  # quebra de página
            p.showPage()
            p.drawImage(caminho_imagem, 0, 0, width=A4[0], height=A4[1])
            y = 680
            p.setFont("Arial", 8)

        # Ordem correta: Código → Descrição → Preço Unitário → Unidade → Quantidade → Taxa → Total
        p.drawString(POSICOES["col_codigo"], y, produto.codigo)
        p.drawString(POSICOES["col_descricao"], y, produto.descricao[:40])
        p.drawRightString(POSICOES["col_preco"], y, f"{produto.preco_unitario:,.2f}")
        p.drawString(POSICOES["col_unid"], y, produto.unidade)
        p.drawRightString(POSICOES["col_qtd"], y, str(produto.quantidade))
        p.drawRightString(POSICOES["col_desc"], y, f"{produto.desconto:.0f}%")
        p.drawRightString(POSICOES["col_subtotal"], y, f"{subtotal:,.2f}")

        y -= 18

    # Forma de pagamento
   
  
    p.drawString(*POSICOES["iban"], f"{IBAN}")

    # Total final
    p.setFont("Arial-Bold", 11)
    p.drawRightString(*POSICOES["total"], f"{total_geral:,.2f} Kz")
    p.setFont("Arial", 9)
    p.drawRightString(*POSICOES["total_p"], f"{total_geral:,.2f} Kz")
    p.drawRightString(*POSICOES["total_p1"], f"{total_geral:,.2f} Kz")
    p.setFont("Arial", 11)
    p.drawRightString(*POSICOES["total_s"], f"{total_geral:,.2f} Kz")

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="proforma_{numero_formatado}.pdf"'
    return response

=======
 
>>>>>>> da0259fcee8726afb712a5afe2ca0ec21dfc0994
class RegisterView(generics.CreateAPIView):
    """
    View para registrar novos usuários.
    """
    queryset = User1.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = serializer.instance
            
            # Geração do token
            refresh = MyTokenObtainPairSerializer.get_token(user)
            access_token = str(refresh.access_token)
            return Response({
                'id': user.id,
                'refresh': str(refresh),
                'access': access_token,
                'expiresIn': 3600  # Duração do token em segundos
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': 'Dados inválidos fornecidos.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Erro ao registrar o usuário. Verifique os dados fornecidos.'}, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    """
    View para obter um par de tokens (access e refresh).
    """
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            tokens = serializer.validated_data
            refresh = tokens['refresh']
            access = tokens['access']
            expires_in = 3600  # Duração do token em segundos
            return Response({
                'id': serializer.user.id,
                'refresh': str(refresh),
                'access': str(access),
                'expiresIn': expires_in
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': 'Erro ao autenticar o usuário.'}, status=status.HTTP_400_BAD_REQUEST)

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar produtos.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(seller=self.request.user)
        except Exception as e:
            return serializer.Exception({'error': 'Erro ao criar produto.'})

class PublicProductListView(generics.ListAPIView):
    """
    View para listar produtos publicamente.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductUpdateView(generics.UpdateAPIView):
    """
    View para atualizar produtos.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            # Verifica se o usuário é o vendedor do produto
            if product.seller != request.user:
                return Response({'error': 'Você não tem permissão para atualizar este produto.'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = self.get_serializer(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar pedidos.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(buyer=self.request.user)
        except Exception as e:
            return serializer.Exception({'error': 'Erro ao criar pedido.'})

class SellerOrdersView(generics.ListAPIView):
    """
    View para listar pedidos do vendedor.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        seller = self.request.user
        return Order.objects.filter(product__seller=seller).select_related('buyer', 'product')

class AdminProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar produtos administrativamente.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class AdminUsersViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar usuários administrativamente.
    """
    queryset = User1.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class AdminOrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar pedidos administrativamente.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
class AdminProductUpdateView(viewsets.ModelViewSet):
    queryset = User1.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] 

    def get(self, request, pk, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SuperUserViewSet(viewsets.ModelViewSet):
    queryset = User1.objects.all()
    serializer_class = SuperUserSerializer
    permission_classes = [IsAdminUser]