import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestAPIRoot:
    def test_api_root_endpoint(self, api_client):
        response = api_client.get(reverse('api-root'))
        assert response.status_code == status.HTTP_200_OK
        assert 'version' in response.data
        assert 'endpoints' in response.data

@pytest.mark.django_db
class TestCustomerAPI:
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        from tests.factories.customer import CustomerFactory
        self.client = api_client
        self.customer = CustomerFactory()
        self.client.force_authenticate(user=self.customer)

    def test_customer_profile(self):
        login_data = {
            'email': self.customer.email,
            'password': 'testpass123'
        }
        login_response = self.client.post('/api/v1/cp/auth/login', login_data)
        token = login_response.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/cp/profile')
        assert response.status_code == status.HTTP_200_OK