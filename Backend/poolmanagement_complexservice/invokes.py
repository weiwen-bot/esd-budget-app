import requests

SUPPORTED_HTTP_METHODS = set([
    "GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"
])

def invoke_http(url, method='GET', json=None, **kwargs):
    """A simple wrapper for requests methods.
       url: the url of the http service;
       method: the http method;
       data: the JSON input when needed by the http method;
       return: the JSON reply content from the http service if the call succeeds;
            otherwise, return a JSON object with a "code" name-value pair.
    """
    #initialise code & result
    code = 200
    result = {}

    try:
        if method.upper() in SUPPORTED_HTTP_METHODS:
            # requests.request invokes the http service
            # saves HTTP response in r
            r = requests.request(method, url, json = json, **kwargs)
        else:
            # raising Exception with message in placeholder
            raise Exception("HTTP method {} unsupported.".format(method))
    except Exception as e:
        # changes code & result
        code = 500
        result = {"code": code, "message": "invocation of service fails: " + url + ". " + str(e)}
    if code not in range(200,300): # unsupported method
        return result

    # check http status code against our request.codes (200)
    if r.status_code != requests.codes.ok:
        code = r.status_code
    try:
        # save the retrieved JSON content
        result = r.json() if len(r.content)>0 else ""
    except Exception as e:
        code = 500
        result = {"code": code, "message": "Invalid JSON output from service: " + url + ". " + str(e)}

    return result

