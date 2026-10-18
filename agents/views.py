from axes.decorators import axes_dispatch
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


@method_decorator(axes_dispatch, name='dispatch')
class AgentLoginView(APIView):
    """Authenticate an agent user using username/password."""

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'login successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'login failed'}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(axes_dispatch, name='dispatch')
class TokenObtainView(APIView):
    """Stub endpoint for token issuance."""

    def post(self, request):
        return Response({'message': 'token endpoint'}, status=status.HTTP_200_OK)


@method_decorator(axes_dispatch, name='dispatch')
class TokenRefreshView(APIView):
    """Stub endpoint for token refresh."""

    def post(self, request):
        return Response({'message': 'refresh endpoint'}, status=status.HTTP_200_OK)


@method_decorator(axes_dispatch, name='dispatch')
class AgentExecuteView(APIView):
    """Stub endpoint for tool execution by an agent."""

    def post(self, request):
        return Response({'message': 'execute endpoint'}, status=status.HTTP_200_OK)


@method_decorator(axes_dispatch, name='dispatch')
class AgentTriggerView(APIView):
    """Stub endpoint for triggering agent workflows."""

    def post(self, request):
        return Response({'message': 'trigger endpoint'}, status=status.HTTP_200_OK)


@method_decorator(axes_dispatch, name='dispatch')
class DataExportView(APIView):
    """Stub endpoint for exporting sensitive data."""

    def post(self, request):
        return Response({'message': 'export endpoint'}, status=status.HTTP_200_OK)


@method_decorator(axes_dispatch, name='dispatch')
class DataUploadView(APIView):
    """Stub endpoint for mutating uploaded data."""

    def post(self, request):
        return Response({'message': 'upload endpoint'}, status=status.HTTP_200_OK)

    def put(self, request):
        return Response({'message': 'upload update endpoint'}, status=status.HTTP_200_OK)


class AgentStatusView(APIView):
    """Read-only status endpoint."""

    def get(self, request):
        return Response({'status': 'active'}, status=status.HTTP_200_OK)


class HealthCheckView(APIView):
    """Health endpoint intentionally excluded from axes protection."""

    def get(self, request):
        return Response({'health': 'ok'}, status=status.HTTP_200_OK)
