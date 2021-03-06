from core.models import Ingredient
from core.models import Recipe
from core.models import Tag
from recipe import serializers
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer


class EmberJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {
            "status_code": renderer_context.get("response"),
            "results": data,
        }
        return super(EmberJSONRenderer, self).render(
            data, accepted_media_type, renderer_context
        )


class BaseView(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Create a new ingredient"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-name")


class TagViewSet(BaseView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseView):
    """Manage ingredients in the database"""

    renderer_classes = (EmberJSONRenderer,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (EmberJSONRenderer,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.RecipeDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
