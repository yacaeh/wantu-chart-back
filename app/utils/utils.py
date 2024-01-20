import requests
import json

from django.http import JsonResponse
import rest_framework.status
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from app.settings import MANDRILL_API_KEY

def jsonify(
    data=None,
    error=None,
    total=None,
    status: rest_framework.status=rest_framework.status.HTTP_200_OK
) -> JsonResponse:
    result = {}
    if data is not None:
        result.update({"data": data})
    if error is not None:
        result.update({"detail": error})
    if total is not None:
        result.update({"total": total})

    return JsonResponse(result, status=status)


def get_body(request):
    return json.loads(request.body.decode("utf-8")) \
        if request.body else {}

def add_allowlist(email):   
    try:
        mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
        response = mailchimp.allowlists.add({"email": email})
        print(response)
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))

def send_email(email, name, template_name):
    try:
        mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
        response = mailchimp.messages.send_template(
            {
                "template_name": template_name,
                'template_content': [{'name': 'user_name', 'content': name}],
                "message": {
                    "subject": name,
                    "from_email": "contact@wantu.io",
                    'to': [{'email': email, 'type': 'to'}], 
                    'subject': '[원투차트]' + name +
                    '님, 24년 1월 3주차 차트가 업데이트 되었습니다.',
                'merge_vars': [
                    {
                        'rcpt': email,
                        'vars': [
                            {
                                'name': 'user_name', 
                                'content': name
                            }
                        ]
                    }
                ]
                }
            }
        )
        print(response)
        print("Send sucessfully")
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))