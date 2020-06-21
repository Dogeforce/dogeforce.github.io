---
title: Salesforce’s Apex does not support the PATCH method. What to do if I need to call an endpoint with PATCH?
author: @renatoliveira
publish_date: 2020-12-25
preview: I needed to call a Microsoft Azure endpoint from Salesforce using the PATCH HTTP verb. The problem is, as mentioned in the title, that Apex does not support this verb.
---
I had a requirement once. A proof of concept. I needed to call a Microsoft Azure endpoint from Salesforce using the PATCH HTTP verb. The problem is, as mentioned in the title, that Apex does not support this verb.

If we are trying to call a Salesforce endpoint, there’s a trick: append `?_HttpMethod=PATCH` to the end of the URL. This is a workaround that Salesforce. This doesn’t help us because we are not calling a Salesforce endpoint. Another workaround would be setting the X-HTTP-Method-Override as PATCH in the request’s header. This is a convention that some servers follow, but this does not guarantee that the server being called will accept our request as a patch.
Let’s write a simple proxy that is hosted on Heroku!

Leveraging a Heroku app in another cloud (technically another Salesforce cloud since 2010) we are able to forward our request to its final destination.

>1. Salesforce calls our Heroku app endpoint
>2. The app forwards the request with the correct verb
>3. The app receives the response from Azure and forwards it back to Salesforce

To do that, I’m going to use Python with the Flask and requests libraries. Flask will handle the “web app” part, while requests is going to be used to forward our request.

NOTE: I am not going to cover the part where we get Azure’s access token because that doesn’t involve an unsupported verb.

Assuming that our Salesforce code will send a request with the access token, the payload and the target URL, it will probably look like this:

    {
        "token": "V2VsbCBhcmVuJ3QgeW91IGN1cmlvdXM/DQoNCiBMb3JlbSBpcHN1bSBkb2xvciBzaXQgYW1ldCwgY29uc2VjdGV0dXIgYWRpcGlzY2luZyBlbGl0LiBOdWxsYW0gcGVsbGVudGVzcXVlIHRvcnRvciBhYyBlbmltIGxhb3JlZXQsIGFjIGVsZW1lbnR1bSB0dXJwaXMgdWx0cmljaWVzLiBJbnRlZ2VyIGludGVyZHVtIHJpc3VzIGxhY3VzLCBlZ2V0IGNvbnNlcXVhdCBsaWd1bGEgZmVybWVudHVtIHZpdGFlLiBFdGlhbSBzb2RhbGVzLCBsaWJlcm8gdml0YWUgZGlnbmlzc2ltIGx1Y3R1cywgbGliZXJvIGFyY3UgdnVscHV0YXRlIHF1YW0sIGF0IG1hdHRpcyBkdWkgbWFnbmEgbmVjIG1hc3NhLiBEb25lYyBpcHN1bSBkb2xvciwgZnJpbmdpbGxhIHZpdGFlIG5pYmggYXQsIHJob25jdXMgc2NlbGVyaXNxdWUgZXN0LiBEb25lYyBuZWMgc29kYWxlcyByaXN1cy4gUGVsbGVudGVzcXVlIHF1aXMgZnJpbmdpbGxhIGVyb3MuIFBlbGxlbnRlc3F1ZSBoYWJpdGFudCBtb3JiaSB0cmlzdGlxdWUgc2VuZWN0dXMgZXQgbmV0dXMgZXQgbWFsZXN1YWRhIGZhbWVzIGFjIHR1cnBpcyBlZ2VzdGFzLiBOYW0gcnV0cnVtIG1ldHVzIG1hdXJpcywgYWMgdWxsYW1jb3JwZXIgdGVsbHVzIGF1Y3RvciBpbi4gVXQgYWNjdW1zYW4gc2NlbGVyaXNxdWUgc29kYWxlcy4gRnVzY2UgdmFyaXVzIG5lcXVlIGVzdCwgc2VkIHB1bHZpbmFyIHNlbSBzY2VsZXJpc3F1ZSBub24uIA==",
        "payload": "IFNlZCB2ZW5lbmF0aXMgZXQgbWV0dXMgbm9uIGx1Y3R1cy4gUGVsbGVudGVzcXVlIGFjIGV1aXNtb2QgbWV0dXMsIG5lYyB0ZW1wb3IgZHVpLiBOYW0gYSB2ZXN0aWJ1bHVtIGZlbGlzLiBOdW5jIG1hZ25hIGxpZ3VsYSwgY29uZ3VlIG5lYyBpbXBlcmRpZXQgdXQsIGNvbmd1ZSB2dWxwdXRhdGUgcXVhbS4gTWFlY2VuYXMgYmxhbmRpdCwgZmVsaXMgbmVjIHNlbXBlciBkYXBpYnVzLCB0ZWxsdXMgaXBzdW0gdm9sdXRwYXQgYXVndWUsIGFjIGVnZXN0YXMgbmlzbCBvcmNpIG5lYyBzYXBpZW4uIEV0aWFtIGEgdnVscHV0YXRlIGVyb3MuIEN1cmFiaXR1ciBsYWNpbmlhIHNjZWxlcmlzcXVlIG5pc2wgc2VkIHZvbHV0cGF0LiBNYXVyaXMgdml0YWUgZXJhdCBwZWxsZW50ZXNxdWUsIGxhY2luaWEgdHVycGlzIHV0LCB0ZW1wb3Igc2FwaWVuLiBJbnRlZ2VyIHZlbCBsb2JvcnRpcyBkdWkuIEN1cmFiaXR1ciBpbXBlcmRpZXQgbWF0dGlzIGZlbGlzLiBQaGFzZWxsdXMgY29tbW9kbyBtYXNzYSBldSB2ZWxpdCBkYXBpYnVzIHRyaXN0aXF1ZSBhIGV1IGxpYmVyby4gRnVzY2UgaW4gcmlzdXMgZW5pbS4gRnVzY2UgZmVybWVudHVtIGV0IHB1cnVzIGV0IGNvbmRpbWVudHVtLiBJbiBzY2VsZXJpc3F1ZSBwb3N1ZXJlIGVsaXQsIHZpdGFlIGludGVyZHVtIHR1cnBpcyBjb25zZWN0ZXR1ciBhdC4g",
        "url": "https://outlook.office.com/api/beta/me/contacts/31d14663-8cf4-4acf-b1c8-556b8e62107d"
    }

The app will receive this and interpret it as “okay, I’ve got this encoded payload, and I shall use this token to send it to this endpoint”:

    # Import the required libraries
    # Flask is the web framework for dealing with web stuff (such as serving the app and handling
    # the connections) We need to import the main "Flask" to run the app, and also its
    # request and Response method and class to handle the request properly
    from flask import Flask, Response, request

    # requests is a simple http request library to handle... requests.
    import requests

    # Base64 is a standard module to help us encode/decode Base 64 strings
    import base64
    # Json is a standar dmodule to help us handle JSON in Python (converting it from/to
    # dictionaries - which are also known as maps in some other languages)
    import json
    # OS is a standard module to handle dealing with the OS directly (we use it just to check
    # an environment variable at the end of the script)
    import os


    # Lets first create the app. This is an empty app which does nothing.
    # The app will do what we want as we define the methods/routes below, with (for example)
    # the `app.route` decorator (which specifies the route and allowed methods)
    app = Flask(__name__)

    # This route defines that the app can receive POST requests in the `/contact/` endpoint. So
    # when deployed, if the app is named `quiet-waters-12345`, its Heroku URL will be
    # `https://quiet-waters-12345.herokuapp.com/` and we should hit that endpoint, adding the
    # `/contact/` at the end.
    @app.route('/contact/', methods=['POST'])
    def contact():
        # First lets deserialize the request's JSON data into a dictionary.
        request_data = request.get_json()

        # We check if there are the required attributes we need
        if 'token' in request_data and 'payload' in request_data and 'url' in request_data:
            try:
                # We try to decode the payload
                payload = base64.b64decode(request_data['payload']).decode('utf-8')

                # Assign the original payload to a new attribute named `original_payload`
                # in our dictionary
                request_data['original_payload'] = payload

                # Define the headers as required by the Azure endpoint
                headers = {
                    'Authorization': 'Bearer ' + request_data['token'],
                    'Content-Type': 'application/json'
                }

                # Try to call external endpoint using the requests library. Note that we
                # use the `patch` method here.
                azure_request = requests.patch(
                    url=request_data['url'],
                    data=payload,
                    headers=headers
                )
                # When the request is finished, its result is stored in `azure_request`,
                # which we can use to get the JSON response.
                result = {
                    "azure_response": azure_request.json()
                }
                # We basically dump the request's result into a new Response and we return
                # it to the service who called us in the first place.
                resp = Response(json.dumps(result), status=azure_request.status_code, mimetype='applcation/json')
                return resp
            except Exception as e:
                resp = Response(json.dumps({'error': e.args}), status=500, mimetype='applcation/json')

        # Returns an error response because there is missing data in the payload.
        return Response(json.dumps({'error':'No token or payload data informed'}), status=400, mimetype='application/json')

    # Checks if the `IS_HEROKU` variable is set. If it is (in our dyno) then the app is running on
    # Heroku's cloud. Otherwise it is running locally in our machine, so we want it to run in our
    # localhost, on port 8080 instead (and with debug mode active).
    if not os.environ.get('IS_HEROKU', None) and __name__ == '__main__':
        app.run(host='localhost', port='8080', debug=True)

And with this small web app hosted in Heroku we are not limited to a single URL. This transforms any POST request to a PATCH request. I’ve used this to call an Outlook endpoint (hence why the apps’ route was named /contacts/) but it can be renamed as needed.

An idea would be to have all HTTP verbs available as endpoints, such as /post, /get, /delete, etc. This way the app will look more like an endpoint bus though…
