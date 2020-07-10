#-*- coding: UTF-8 -*-
import revitron
import re


class AttrDict(dict):
    """A dict whose items can also be accessed as member variables.
    
    http://code.activestate.com/recipes/361668/
    
    >>> d = attrdict(a=1, b=2)
    >>> d['c'] = 3
    >>> print d.a, d.b, d.c
    1 2 3
    >>> d.b = 10
    >>> print d['b']
    10

    # but be careful, it's easy to hide methods
    >>> print d.get('c')
    3
    >>> d['get'] = 4
    >>> print d.get('a')
    Traceback (most recent call last):
    TypeError: 'int' object is not callable
    """
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
        
        
class String:
    
    @staticmethod
    def sanitize(string):
        string = string.replace('ü', 'ue')
        string = string.replace('Ü', 'Ue')
        string = string.replace('ö', 'oe')
        string = string.replace('Ö', 'Oe')
        string = string.replace('ä', 'ae')
        string = string.replace('Ä', 'Ae')
        string = re.sub('[^a-zA-Z0-9_\-]', '_', string)
        string = re.sub('_+', '_', string) 
        string = re.sub('(-_|_-)', '-', string)
        return string