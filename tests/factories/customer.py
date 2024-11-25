import factory
from django.contrib.auth import get_user_model

class CustomerFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = get_user_model()
    # skip_postgeneration_save = True

  email = factory.Sequence(lambda n: f'user{n}@example.com')
  password = factory.PostGenerationMethodCall('set_password', 'testpass123')
  first_name = factory.Faker('first_name')
  last_name = factory.Faker('last_name')
  phone = factory.Sequence(lambda n: f'+1{str(n).zfill(10)}')
  country = factory.Faker('country_code')
  status = 'active'