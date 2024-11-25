import pytest
from django.contrib.auth import get_user_model
from django.conf import settings

Customer = get_user_model()

@pytest.mark.django_db
class TestCustomerModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.customer = Customer.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            phone='+1234567890',
            country='US',
            status='active'
        )

    def test_customer_creation(self):
        assert self.customer.email == 'test@example.com'
        assert self.customer.check_password('testpass123')

    def test_customer_str_representation(self):
        assert str(self.customer) == 'test@example.com'

    @pytest.mark.asyncio
    async def test_customer_elasticsearch_index(self, es_test_client):
        from core.elasticsearch.indices.customer import CustomerIndex
        from asgiref.sync import sync_to_async
        
        # Get document synchronously since it's a simple model method
        doc = CustomerIndex.get_document(self.customer)
        
        # Use the async client properly
        await es_test_client.index(
            index=f"{settings.ELASTICSEARCH_INDEX_PREFIX}_customers",
            id=str(self.customer.id),
            document=doc,
            refresh=True
        )
        
        result = await es_test_client.get(
            index=f"{settings.ELASTICSEARCH_INDEX_PREFIX}_customers",
            id=str(self.customer.id)
        )
        assert result['_source']['email'] == self.customer.email