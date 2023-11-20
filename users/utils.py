import jwt

from django.http      import JsonResponse

from app.settings      import SECRET_KEY
from users.models     import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            user         = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
            request.user = User.objects.get(id = user['id'])

        except jwt.exceptions.DecodeError:                                   
            return JsonResponse({'message' : '일치하지 않는 토큰입니다.' }, status=400)

        except User.DoesNotExist:       
            return JsonResponse({'message' : '존재하지 않는 사용자입니다.'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper


def encode_jwt(data):
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')


def decode_jwt(access_token):
    return jwt.decode(
        access_token,
        SECRET_KEY,
        algorithms=['HS256'],
    )


def get_user_by_request(request):
    try:
        access_token = request.META.get("HTTP_AUTHORIZATION", None)
        print("GET ACCESS TOEKN", access_token)
        payload = decode_jwt(access_token)
        user_id = payload.get("id", None)

        return User.objects.get(id=user_id)

    except Exception:
        return None
