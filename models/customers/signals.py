from asgiref.sync import async_to_sync
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import asyncio
from core.elasticsearch.client import es_client
from .models import Customer
from core.elasticsearch.indices import CustomerIndex

@receiver(post_save, sender=Customer)
def index_customer(sender, instance, created, **kwargs):
  try:
    loop = asyncio.get_event_loop()
  except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
  
  loop.run_until_complete(es_client.add_document(
    index=CustomerIndex.get_index_name(),
    id=str(instance.id),
    document=CustomerIndex.get_document(instance)
  ))

@receiver(post_delete, sender=Customer)
def delete_customer_index(sender, instance, **kwargs):
  async_to_sync(es_client.delete_document)(
    index=CustomerIndex.get_index_name(),
    id=str(instance.id)
  ) 

  
