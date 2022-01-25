from collections import OrderedDict

class Cache:
    """lru cache except you can manually add to the cache"""
    def __init__(self, func, maxsize=1e5):
        self.func = func
        self.cache = OrderedDict()
        self.maxsize = maxsize
    
    def _shrink(self):
        """Removes the oldest items from the cache"""
        while len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
    
    def save(self, new: dict):
        """Updates the cache with values from a dictionary"""
        for key, val in new.items():
            self.cache[key] = val
        self._shrink()
    
    def __call__(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            value = self.cache[key]
            cache_hit = True
        else:
            value = self.func(key)
            self.cache[key] = value
            self._shrink()
            cache_hit = False
        
        return {"cached": cache_hit, **value}
