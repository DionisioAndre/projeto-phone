
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Product, Order
from .serializers import RegisterSerializer,MyTokenObtainPairSerializer, ProductSerializer, OrderSerializer, UserSerializer,SuperUserSerializer
import logging


 
class RegisterView(generics.CreateAPIView):
    """
    View para registrar novos usuários.
    """
    queryset = User.objects.all()
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
    queryset = User.objects.all()
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
    queryset = User.objects.all()
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
    queryset = User.objects.all()
    serializer_class = SuperUserSerializer
    permission_classes = [IsAdminUser]