import json
import re
import bcrypt, jwt
from json.decoder           import JSONDecodeError

from django.http            import JsonResponse
from django.views           import View
from django.http.response   import HttpResponse, JsonResponse

from users.utils            import login_decorator, get_user_by_request
from users.models           import User
from movies.models          import Rating, WishList, PlayHistory
from app.settings      import SECRET_KEY
import users.serializers as serializers

from app.utils.youtube import convert_PT_to_time

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            image   = data['image']
            # password = data['password']
            # image_url = data['image_url']
            google_token = data['google_token']

            if google_token is None:
                return JsonResponse({'MESSAGE' : 'No google Token Found'}, status=400)

            # if not re.match('^[a-zA-Z가-힣]{2,}$', name):
            #     return JsonResponse({'MESSAGE' : 'Wrong Name Form'}, status=400)

            if not re.match('^[a-zA-Z\d+-.]+@[a-zA-Z\d+-.]+\.[a-zA-Z]{2,3}$', email):
                return JsonResponse({'MESSAGE' : 'Wrong E-mail Form'}, status=400)

            # if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{10,}$',password):
            #     return JsonResponse({'MESSAGE' : 'Wrong Password Form'}, status=400)

            if User.objects.filter(email=email).exists():
                current_user = User.objects.get(email=email)
                current_user.google_token = google_token
                current_user.image_url = image
                current_user.name = name
                current_user.save()
                token = jwt.encode({"id" : current_user.id}, SECRET_KEY, algorithm='HS256')
                print(token)

                return JsonResponse({
                    "MESSAGE"    : "accepted",
                    "auth_token" : token,
                    "user_name"  : current_user.name,
                    "google_token" : current_user.google_token,
                    "user_id"    : current_user.pk,
                }, status=200)

            # decoded_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            current_user = User.objects.create(
                name     = name,
                email    = email,
                image_url = image,
                google_token = google_token,
            )
            token = jwt.encode({"id" : current_user.pk}, SECRET_KEY, algorithm='HS256')
            print(token)

            return JsonResponse({
                    'MESSAGE' : 'User Registered!',
                    "auth_token" : token,
                    "user_name"  : current_user.name,
                    "google_token" : current_user.google_token
                }, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)


class Login(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"MESSAGE" : "존재하지 않는 아이디입니다!"}, status=401)

            current_user = User.objects.get(email=data['email'])
            
            if not bcrypt.checkpw(data['password'].encode(), current_user.password.encode()):
                return JsonResponse({"MESSAGE" : "비밀번호가 일치하지 않습니다!"}, status=401)
                
            token = jwt.encode({"id" : current_user.id}, SECRET_KEY, algorithm='HS256')
            
            return JsonResponse({
                "MESSAGE"    : "accepted",
                "auth_token" : token,
                "user_name"  : current_user.name
            }, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"MESSAGE" : "VALUE ERROR"}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({"MESSAGE" : "INVALID DATA FORMAT"}, status=400)


class RatingsView(View):
    print("Rating view called???")
    def get(self, request, user_id):
        my_user = get_user_by_request(request) or None
        user = User.objects.get(id=user_id)
        is_mine = False
        if my_user is not None:
            is_mine = True if my_user.id == user_id else False


        ratings = Rating.objects.filter(user_id=user_id).order_by('-id')[:10]
        print(ratings.count())
        if ratings:
            comment_list = [{
                "user_name"   : rating.user.name, 
                "user_image"  : rating.user.image_url,
                "user_id"     : rating.user.id,
                "comment"     : rating.comment, 
                "user_rating" : rating.rate ,
                "spoiler"     : rating.spoiler,
                "series"      : rating.movie.title,
                "trailer"     : rating.movie.trailer,
                "movie_id"    : rating.movie.id,
            }for rating in ratings]
            
            return JsonResponse({"results" : comment_list, "total":ratings.count(), "is_mine":is_mine}, status=200)
        
        return HttpResponse('NO CONTENTS', status=204)

class MyRatingsView(View):
    print("My rating View Called")
    @login_decorator
    def get(self, request):
        movie_list = []
        print("Requested from..",request.user.id)
        print("Requested from..",request.user.name)
        movies = Rating.objects.select_related('movie').filter(user_id=request.user.id)

        if movies:
            movie_list : [{
                "country_name"   : [country.name for country in movie.country.all()],
                "movie_name"     : movie.title,
                "movie_id"       : movie.id,
                # "running_time"   : sum([convert_PT_to_time(episode.duration) for episode in movie.episode.all()]),
                # "total_views"     : sum([episode.viewCount for episode in movie.episode.all()]),
                # "total_likes"     : sum([episode.likeCount for episode in movie.episode.all()]),
                # "total_comments"  : sum([episode.commentCount for episode in movie.episode.all()]),
                # "total_episodes"  : movie.episode.count(),
                "released_date"  : movie.release_date,
                "average_rating" : movie.average_rating,
                "poster_image"   : movie.poster_image,
                "trailer"        : movie.trailer,
                "genres"         : [genre.name for genre in movie.genre.all()],
            } for movie in movies]

            return JsonResponse({"results" : movie_list}, status=200)
        
        return HttpResponse('NO CONTENTS', status=204)


class WishlistView(View):
    def get(self, request, user_id):
        my_user = get_user_by_request(request) or None
        user = User.objects.get(id=user_id)
        movies = WishList.objects.select_related('movie').filter(user_id=user_id)
        is_mine = False
        if my_user is not None:
            is_mine = True if my_user.id == user_id else False

        if movies:
            wish_movies = [{
                "movie_name"     : movie.movie.title,
                "movie_id"       : movie.movie.id,
                "released_date"  : movie.movie.release_date,
                "average_rating" : movie.movie.average_rating,
                "poster_image"   : movie.movie.poster_image
            }for movie in movies]
                
            return JsonResponse({"results" : wish_movies, "total": movies.count(), "is_mine":is_mine}, status=200)
        
        return HttpResponse('NO CONTENTS', status=204)

class MyWishlistView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        movie_id = data['movie_id']
        try:
            wishlist = WishList.objects.get(
                user_id=request.user.id,
                movie_id=movie_id,
            )
            wishlist.delete()

        except WishList.DoesNotExist:
            wishlist = WishList.create(data={
                'user_id': request.user.id,
                'movie_id':movie_id,
            })
            if wishlist.is_valid():
                wishlist.save()
                return JsonResponse({"MESSAGE" : "Saved"}, status=201)

            else:
                return JsonResponse({"MESSAGE" : "KEY ERROR"}, status=400)


        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"MESSAGE" : "VALUE ERROR"}, status=400)
        return JsonResponse({"MESSAGE" : "KEY ERROR"}, status=400)

    @login_decorator
    def get(self, request):
        print("Requested from..",request.user.id)
        print("Requested from..",request.user.name)

        movies = WishList.objects.select_related('movie').filter(user_id=request.user.id)

        if movies:
            wish_movies = [{
                "movie_name"     : movie.movie.title,
                "movie_id"       : movie.movie.id,
                "released_date"  : movie.movie.release_date,
                "average_rating" : movie.movie.average_rating,
                "poster_image"   : movie.movie.poster_image
            }for movie in movies]
                
            return JsonResponse({"results" : wish_movies}, status=200)

        return HttpResponse('NO CONTENTS', status=204)

class Profile(View):
    def get(self, request, user_id):
        my_user = get_user_by_request(request) or None
        print("USER ID = ",user_id, my_user)
        print("MY USER OBJECT = ",get_user_by_request(request))
        user = User.objects.get(id=user_id)
        print("USER OBJECT = ", user)
        user_detail = serializers.UserDetailSerializer(user, context={'my_user': my_user}).data
        print(user_detail)

        return JsonResponse({"result" : user_detail}, status=200)
    

class MyPlayHistoryView(View):
    @login_decorator
    def get(self, request):
        user_id = request.user.id
        play_history = PlayHistory.objects.filter(user_id=user_id)
        print(play_history)
        history_list = [{
            "movie_id" : h.movie.id,
            "movie_name"    : h.movie.title,
            "average_rating"      : h.movie.average_rating,
            "poster_image"   : h.movie.poster_image,
            "trailer"  : h.movie.trailer,
            "last_played"     : h.last_played,
            "episode_name" : h.episode.name,
        }for h in play_history]
        print(history_list)
        return JsonResponse({"result" :history_list}, status=200)
