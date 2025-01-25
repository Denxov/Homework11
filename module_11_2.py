import sys
class FirstClass:
    def method(self):
        pass
def introspection_info(obj):
    specs={}
    specs['Type']=type(obj)
    specs['Value']=obj
    if '__len__' in obj.__dir__():
        specs['length']=len(obj)
    if '__module__' in obj.__dir__():
        specs['Module'] = obj.__module__
    specs['Methods'] = [method_name for method_name in dir(obj) if callable(getattr(obj, method_name)) and not method_name.startswith('__') ]
    return specs

print(introspection_info(12))
print(introspection_info('dee'))
print(introspection_info(introspection_info))
print(introspection_info(FirstClass()))
