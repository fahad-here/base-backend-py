import pytest
from asgiref.sync import sync_to_async
from tests.factories.customer import CustomerFactory
from core.elasticsearch.indices.customer import CustomerIndex
from django.conf import settings

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_customer_indexing(es_test_client):
    # Create customer using sync_to_async since factory is synchronous
    customer = await sync_to_async(CustomerFactory)()
    
    doc = CustomerIndex.get_document(customer)
    await es_test_client.index(
        index=f"{settings.ELASTICSEARCH_INDEX_PREFIX}_customers",
        id=str(customer.id),
        document=doc,
        refresh=True
    )
    
    search_result = await es_test_client.search(
        index=f"{settings.ELASTICSEARCH_INDEX_PREFIX}_customers",
        query={"match": {"email": customer.email}}
    )
    assert search_result['hits']['total']['value'] == 1