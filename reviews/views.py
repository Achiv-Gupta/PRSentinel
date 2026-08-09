from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import process_pull_request


@api_view(["POST"])
def github_webhook(request):
    files = process_pull_request(request.data)

    if files:
        for file in files:
            print(file["filename"])
            print(file["patch"])

    return Response({"message": "Webhook received"})