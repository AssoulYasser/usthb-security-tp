from django.test import TestCase
from django.core.cache import cache


# Create your tests here.
class CacheTest(TestCase):
    print('gg')
    cache.set('key', {'a': 1, 'b': 2}, timeout=90)
    value = cache.get('key')
    print(value)
    cache.get('key')['c'] = 5
    value = cache.get('key')
    print(value)