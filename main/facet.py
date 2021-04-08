import json
import re
import numpy as np

def from_camel(attr):
    """convert thisAttrName to this_attr_name."""
    # Don't add an underscore for capitalized first letter
    return re.sub(r'(?<=.)([A-Z])', lambda x: '_' + x.group(1), attr).lower()

def to_camel(attr):
    """convert this_attr_name to thisAttrName."""
    # Do lower case first letter
    return (attr[0].lower() + re.sub(r'_(.)', lambda x: x.group(1).upper(), attr[1:]))

class Facet(object):
    def __init__(self, column, facet_type, **options):
        self.type = facet_type
        self.name = column
        self.column_name = column
        for k, v in options.items():
            setattr(self, k, v)

    def as_dict(self):
        return dict([(to_camel(k), v) for k, v in self.__dict__.items()
                     if v is not None])


class TextFilterFacet(Facet):
    def __init__(self, column, query, **options):
        super(TextFilterFacet, self).__init__(
            column, query=query, case_sensitive=False, facet_type='text',
            mode='text', **options)


class TextFacet(Facet):
    def __init__(self, column, selection=None, expression='value',
                 omit_blank=False, omit_error=False, select_blank=False,
                 select_error=False, invert=False, **options):
        super(TextFacet, self).__init__(
            column,
            facet_type='list',
            omit_blank=omit_blank,
            omit_error=omit_error,
            select_blank=select_blank,
            select_error=select_error,
            invert=invert,
            **options)
        self.expression = expression
        self.selection = []
        if selection is None:
            selection = []
        elif not isinstance(selection, list):
            selection = [selection]
        for value in selection:
            self.include(value)

    def include(self, value):
        for s in self.selection:
            if s['v']['v'] == value:
                return
        self.selection.append({'v': {'v': value, 'l': value}})
        return self

    def exclude(self, value):
        self.selection = [s for s in self.selection
                          if s['v']['v'] != value]
        return self

    def reset(self):
        self.selection = []
        return self




