from axes.utils import reset
from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework.test import APITestCase


@override_settings(AXES_FAILURE_LIMIT=3, AXES_COOLOFF_TIME=None)
class AgentSecurityTests(APITestCase):
    def setUp(self):
        self.username = 'test_agent'
        self.password = 'StrongPass123!'
        User.objects.create_user(username=self.username, password=self.password)
        self.login_url = '/agents/api/auth/login/'
        self.health_url = '/agents/api/health/'
        self.status_url = '/agents/api/agents/status/'
        reset()

    def test_health_and_status_are_available(self):
        health_response = self.client.get(self.health_url)
        status_response = self.client.get(self.status_url)
        self.assertEqual(health_response.status_code, 200)
        self.assertEqual(status_response.status_code, 200)

    def test_sequential_failed_logins_transition_to_lockout(self):
        responses = []
        for _ in range(4):
            response = self.client.post(
                self.login_url,
                {'username': self.username, 'password': 'WrongPassword!'},
                REMOTE_ADDR='198.51.100.10',
                format='json',
            )
            responses.append(response.status_code)

        self.assertEqual(responses[:3], [401, 401, 401])
        self.assertEqual(responses[3], 403)

    def tearDown(self):
        reset()
