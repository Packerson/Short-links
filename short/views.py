from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from short import models as short_models
from short import serializers as short_serializers


class ToShortenView(APIView):
    """
    View for shortening a URL
    """
    serializer_class = short_serializers.ShortenInputSerializer
    output_serializer = short_serializers.ShortenOutputSerializer

    def post(self, request):
        # validate data
        input_serializer = self.serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        # get/create short link
        short_link, created = input_serializer.save()

        # status code based on created
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        return Response(
            self.output_serializer(short_link).data,
            status=status_code,
        )


class ToReadView(RetrieveAPIView):
    """
    View for reading a URL by short code.
    """
    queryset = short_models.ShortLink.objects.all()
    serializer_class = short_serializers.ReadOutputSerializer
    lookup_field = "code"
    lookup_url_kwarg = "code"