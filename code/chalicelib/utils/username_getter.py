def get_authorized_username(current_request):
    return current_request.context["authorizer"]["principalId"]
