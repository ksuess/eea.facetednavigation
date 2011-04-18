""" Caching module
"""
from eea.facetednavigation.caching.cache import cacheKeyFacetedNavigation
from eea.facetednavigation.caching.cache import cacheCounterKeyFacetedNavigation
try:
    from eea.cache import cache
    from lovely.memcached import event
    ramcache = cache
    InvalidateCacheEvent = event.InvalidateCacheEvent
except ImportError:
    # Fail quiet if required cache packages are not installed in order to use
    # this package without caching
    from eea.facetednavigation.caching.nocache import ramcache
    from eea.facetednavigation.caching.nocache import InvalidateCacheEvent

__all__ = [
    cacheKeyFacetedNavigation.__name__,
    cacheCounterKeyFacetedNavigation.__name__,
    ramcache.__name__,
    InvalidateCacheEvent.__name__,
]
