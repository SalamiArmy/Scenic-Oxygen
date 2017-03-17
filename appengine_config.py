from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
try:
    vendor.add('lib')
except:
    print('Failed to add thrid-party libs to app engine instance.')
