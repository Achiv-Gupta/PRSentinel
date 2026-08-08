from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def github_webhook(request):
    print(request.data)

    return Response({"message": "Webhook received"})
