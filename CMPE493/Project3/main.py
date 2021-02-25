import os, sys
from urllib.parse import urlparse

# REFERENCE: https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
# Checks whether the given input is a URL.
def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

userArg = sys.argv[1]

# If the user enters a URL, then it is considered as a query. Otherwise, the entire recommendation
# system has been built from scratch.
if uri_validator(userArg):
    queryCommand = 'python3 query.py {}'.format(userArg)
    os.system(queryCommand)
else:
    trainingCommand = 'python3 training.py {}'.format(userArg)
    os.system(trainingCommand)