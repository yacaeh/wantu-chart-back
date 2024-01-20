import json
from json.decoder import JSONDecodeError
from decimal import *

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db.models import Q, Avg
from django.core.exceptions import ValidationError

from users.utils import login_decorator
from movies.models import Movie, MovieParticipant, Channel, Rating, MovieGenre, MovieEpisode, Episode, Genre, Country, WishList, PlayHistory
from movies.serializers import EpisodeSerializer
from django.shortcuts import render
from app.utils.youtube import get_channel_info, get_video_details,get_playlist_info, get_comments, get_highlights, comment, convert_PT_to_time
from datetime import datetime
from typing import Iterable
from collections import namedtuple
from bulk_update_or_create import BulkUpdateOrCreateQuerySet
import re
from datetime import datetime, timedelta
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

ManyToManySpec = namedtuple(
    "ManyToManySpec", ["from_object", "to_object"]
)


def bulk_create_manytomany_relations(
    model_from,
    field_name: str,
    model_from_name: str,
    model_to_name: str,
    specs: Iterable[ManyToManySpec]
):
    through_objs = []
    for spec in specs:
        through_objs.append(
            getattr(model_from, field_name).through(
                **{
                    f"{model_from_name.lower()}_id": spec.from_object.id,
                    f"{model_to_name.lower()}_id": spec.to_object.id,
                }
            )
        )
    getattr(model_from, field_name).through.objects.bulk_create(through_objs)

class ChannelView(View):
    @method_decorator(cache_page(60*60*24))
    def get(self, request):
        OFFSET = 0
        LIMIT  = 16

        channels = Channel.objects.all().order_by('-subscriber_count')
        channel_list = [{
            "id": channel.id,
            "channel_id"       : channel.channel_id,
            "handle"           : channel.handle,
            "title"            : channel.title,
            "description"      : channel.description,
            "published_at"     : channel.published_at,
            "thumbnail"        : channel.thumbnail,
            "view_count"       : channel.view_count,
            "subscriber_count" : channel.subscriber_count,
            "video_count"      : channel.video_count,
        } for channel in channels][OFFSET : LIMIT]

        return JsonResponse({"results" : channel_list}, status=200)
        # return HttpResponse('<html><body> channel ... cached</body></html>')

class ChannelDetailView(View):
    @method_decorator(cache_page(60*60*24))
    def get(self, request, channel_id):
        try:
            if not Channel.objects.filter(id=channel_id).exists():
                return JsonResponse({'MESSAGE' : 'Channel Not Exists'}, status = 404)

            channel = Channel.objects.get(id=channel_id)

            channel_details = {
                'channel_id'       : channel_id,
                'title'          : channel.title,
                'description'      : channel.description,
                'handle'           : channel.handle,
                'published_at'   : channel.published_at,
                'thumbnail'        : channel.thumbnail,
                'movie_list' : [{
                    "country_name"   : [country.name for country in movie.country.all()],
                    "movie_name"     : movie.title,
                    "movie_id"       : movie.id,
                    "running_time"   : sum([convert_PT_to_time(episode.duration) for episode in movie.episode.all()]),
                    "total_views"     : sum([episode.viewCount for episode in movie.episode.all()]),
                    "total_likes"     : sum([episode.likeCount for episode in movie.episode.all()]),
                    "total_comments"  : sum([episode.commentCount for episode in movie.episode.all()]),
                    "total_episodes"  : movie.episode.count(),
                    "released_date"  : movie.release_date,
                    "average_rating" : movie.average_rating,
                    "poster_image"   : movie.poster_image,
                    "trailer"        : movie.trailer,
                    "genres"         : [genre.name for genre in movie.genre.all()],
                } for movie in Movie.objects.filter(channel_id=channel_id)]
            }

            return JsonResponse({'channel_info' : channel_details}, status = 200)

        except KeyError:
            JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)


class MovieView(View): 
    @method_decorator(cache_page(60*60*24))
    def get(self,request): 
        search = request.GET.get('search', '')
        country_name  = request.GET.get("country")
        genre1        = request.GET.get("genre1")
        genre2        = request.GET.get("genre2")
        rating        = request.GET.get("rating","")
        KOREAN_MOVIE  = "한국"
        FOREIGN_MOVIE = "외국"
        LIMIT         = 25
        OFFSET        = 0

        q = Q()
        
        if genre1 == "전체":
            genre1 = ""
        if country_name == KOREAN_MOVIE:
            q.add(Q(country__name=KOREAN_MOVIE), q.AND)

        if country_name == FOREIGN_MOVIE:
            q.add(~Q(country__name=KOREAN_MOVIE), q.AND)

        if genre1 or genre2:
            q.add(Q(genre__name=genre1)|Q(genre__name=genre2), q.AND)
        
        movies = Movie.objects.filter(q).order_by('-release_date').distinct()
        
        if search:
            movies = movies.filter(
                Q(description__icontains=search) | Q(title__icontains=search)
            ).distinct()

        if rating:
            movies =  Movie.objects.order_by('-average_rating')


        movie_list = [{
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
        } for movie in movies ][OFFSET : LIMIT]

        return JsonResponse({"results" : movie_list, "page":OFFSET}, status=200)


class RateView(View):
    @login_decorator
    def post(self, request, movie_id):
        try:
            data = json.loads(request.body)
            print(request.body)
            print(data)
            rate = data['rate']

            Rating.objects.update_or_create(
                user_id  = request.user.id,
                movie_id = movie_id,
                defaults = {'rate' : rate}
            )

            mv_rate  = Rating.objects.filter(movie_id=movie_id)
            avg_rate = mv_rate.aggregate(avg_rate=Avg('rate'))
            
            Movie.objects.filter(id=movie_id).update(average_rating=avg_rate['avg_rate'])


            return JsonResponse({
                "message" : "SUCCESS"
            }, status=200)

        except KeyError:
            return JsonResponse({"message" : "INVALID FORMAT"}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({"message" : "NO DATA"}, status=400)
        
        except ValidationError:
            return JsonResponse({"message" : "TYPE DOESNT MATCH"}, status=400)
    
    @login_decorator
    def get(self, request, movie_id):
        
        if Rating.objects.filter(user_id=request.user.id, movie_id=movie_id).exists():
                rate = Rating.objects.get(user_id=request.user.id, movie_id = movie_id).rate
        else:
            rate = 0.0

        return JsonResponse({"user_rate" : rate}, status=200)


class GenreMovieView(View):

    @method_decorator(cache_page(60*60*24))
    def get(self, request):  
        OFFSET = 0
        LIMIT  = 16
        q      = Q()

        try:
            movie_id = request.GET.get('id', None)
            
            if not movie_id:
                return JsonResponse({"message" : "NO QUERY STRING"}, status=404)  
            
            if not MovieGenre.objects.filter(movie_id=movie_id).exists():
                return JsonResponse({"message" : "QUERY DOES NOT MATCH"}, status=404)

            genres = MovieGenre.objects.filter(movie_id=movie_id)

            related = []

            for genre in genres:
                q |= Q(genre__id = genre.genre_id)
            
            movie = MovieGenre.objects.select_related('movie').filter(q).exclude(movie_id=movie_id)
            
            related = [{
                "movie_id" : mv.movie.id,
                "title"    : mv.movie.title,
                "avg"      : mv.movie.average_rating,
                "poster"   : mv.movie.poster_image,    
            }for mv in movie]
            
            related_movies = list({rel['title']: rel for rel in related}.values())
            
            return JsonResponse({
                "message" : "SUCCESS",
                "related_movies" : related_movies[OFFSET:LIMIT],
            },status=200)
        
        except KeyError:
            return JsonResponse({"message": "INVALID DATA FORMAT"}, status=400)


class MovieDetailView(View):

    @method_decorator(cache_page(60*60*24))
    def get(self, request, movie_id):
        try:
            if not Movie.objects.filter(id=movie_id).exists():
                return JsonResponse({'MESSAGE' : 'Movie Not Exists'}, status = 404)

            movie = Movie.objects.get(id=movie_id)
            print(movie)
            movie_details = {
                'movie_id'       : movie_id,
                'title'          : movie.title,
                'released_date'   : movie.release_date,
                'genres'         : [genre.name for genre in movie.genre.all()],
                'country'        : [country.name for country in movie.country.all()],
                'poster_image'   : movie.poster_image,
                'trailer'        : movie.trailer,
                'image_url'      : [image.image_url for image in movie.image_set.all()],
                # 'participants'   : [
                #     {
                #         'name'  : participants.participant.name,
                #         'role'  : participants.role,
                #         'image' : participants.participant.image_url 
                #     } for participants in MovieParticipant.objects.filter(movie=movie_id)
                # ],
                'description'    : movie.description,
                'rating_users'   : movie.rating_set.count(),
                'average_rating' : movie.average_rating,
                'is_new'         : movie.is_new,
                'is_wish'        : WishList.objects.filter(user_id=request.user.id, movie_id=movie_id).exists(),
            }

            return JsonResponse({'movie_info' : movie_details}, status = 200)

        except KeyError:
            print("KeyError")
            print(KeyError)
            JsonResponse({'MESSAGE' : KeyError}, status=400)



class CommentView(View):
    @login_decorator
    def post(self, request, movie_id):
        try:    
            data    = json.loads(request.body)
            user_id = request.user.id
            rating  = Rating.objects.get(user_id=user_id,movie_id=movie_id)
            print(data)
            if not rating:
                return JsonResponse({"MESSAGE" : "ENTER_RATING_FIRST"}, status=404)

            rating.comment = (data["comment"])
            rating.save()

            movie = Movie.objects.get(id=movie_id)
            text = "원투에서 작성한 리뷰 입니다. \n원투 평점 : " + str(rating.rate)+"/5" + "점\n" + data['comment']
            # Comment on Youtube As well
            comment(movie.trailer, text, request.user.google_token)

            return JsonResponse({"MESSAGE" : "CREATE"}, status=200)
        except ValueError:
                return JsonResponse({"MESSAGE" : "VALUE_ERROR"}, status=404)
        except KeyError:
                return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=404)

    def get(self, request, movie_id):
        comment_list = [{
            "user_name"   : rating.user.name, 
            "user_image"  : rating.user.image_url,
            "user_id"     : rating.user.id,
            "comment"     : rating.comment, 
            "user_rating" : rating.rate ,
            "spoiler"     : rating.spoiler,
        }for rating in Rating.objects.filter(movie_id=movie_id).order_by('-id')]

        return JsonResponse({"result" :comment_list}, status=200)

class EpisodeMovieView(View):
    @method_decorator(cache_page(60*60*24))
    def get(self, request, movie_id):
        episode_ids = MovieEpisode.objects.filter(movie_id=movie_id).values_list('episode_id', flat=True)
        episode_list = Episode.objects.filter(pk__in=episode_ids).exclude(name='Private video')
        serialized_episodes = EpisodeSerializer(episode_list, many=True)
        
        return JsonResponse({
            "message" : "SUCCESS",
            "episodes" : serialized_episodes.data,
        },status=200)


class WishListView(View):
    @login_decorator
    def post(self, request, movie_id):
        try:    
            data    = json.loads(request.body)
            user_id = request.user.id
            wishlist  = WishList.objects.get(user_id=user_id,movie_id=movie_id)
            isDelete = data['isDelete']
            
            if not isDelete:
                wishlist.save()
                return JsonResponse({"MESSAGE" : "ADDED TO Wishlist"}, status=200)
            
            else:
                wishlist.delete()
                return JsonResponse({"MESSAGE" : "REMOVED FROM Wishlist"}, status=200)
            
        except WishList.DoesNotExist:
                WishList.objects.create(user_id=user_id, movie_id=movie_id)
                print("Added to wishlist")
                return JsonResponse({"MESSAGE" : "ADDED TO Wishlist"}, status=200)

        except ValueError:
                return JsonResponse({"MESSAGE" : "VALUE_ERROR"}, status=404)
        except KeyError:
                return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=404)

    @login_decorator
    def get(self, request, movie_id):
        try:    
            print("Wishlist called")
            user_id = request.user.id
            wishlist  = WishList.objects.get(user_id=user_id,movie_id=movie_id)
            if not wishlist:
                print("no wishlist found...")
                return JsonResponse({"MESSAGE" : "No Wishlist"}, status=200)
            
            else:
                print("Wishlist exist!")
                return JsonResponse({"is_wish" : True}, status=200)

        except WishList.DoesNotExist:
                print("no wishlist found...")
                return JsonResponse({"is_wish" : False}, status=200)

        except ValueError:
                return JsonResponse({"MESSAGE" : "VALUE_ERROR"}, status=404)
        except KeyError:
                return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=404)


import csv
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect


def channel_upload_from_csv(request):
    if request.method == "GET":
        return render(request,'channel_upload_csv.html')
    if request.method == "POST":
        file = request.FILES['csv_file']

        if not file.name.endswith(".csv"):
            messages.error(request, '파일이 csv 형식이 아닙니다.')
            return redirect('channel_upload_from_csv')

        decoded_file = file.read().decode('utf-8').splitlines()
        rdr = csv.reader(decoded_file)
        info = []
        channel_ids = []

        for row in rdr:
            name, handle, channelId,_,_ = row
            # tuple = (name, handle, channelId)
            # info.append(tuple)
            channel_ids.append(channelId)
        file.close()

        instances = []
        del channel_ids[0]
        print(channel_ids)
        data = get_channel_info(channel_ids)

        for youtube in data:
            channel_id  = youtube['id']
            title = youtube['snippet']['title']
            description = youtube['snippet']['description']
            customUrl = youtube['snippet']['customUrl']
            publishedAt = youtube['snippet']['publishedAt']
            thumbnail = youtube['snippet']['thumbnails']['high']['url']
            viewCount = youtube['statistics']['viewCount']
            subscriberCount = youtube['statistics']['subscriberCount']
            videoCount = youtube['statistics']['videoCount']
            instances.append(Channel(title=title,handle=customUrl, channel_id=channel_id, description=description, published_at=publishedAt, thumbnail=thumbnail, view_count=viewCount, subscriber_count=subscriberCount, video_count=videoCount))

        try:
            Channel.objects.bulk_update_or_create(instances, ['title','handle','channel_id','description', 'published_at', 'thumbnail','view_count','subscriber_count', 'video_count'], match_field='channel_id')
        except IntegrityError:
            messages.error(request, '등록된 채널과 중복된 정보가 있습니다.')
            return redirect('channel_upload_from_csv')
        else:
            messages.info(request,"성공적으로 등록되었습니다.")
            return redirect("channel_list")
        
def movie_upload_from_csv(request):
    if request.method == "GET":
        return render(request,'playlist_upload_csv.html')
    if request.method == "POST":
        file = request.FILES['csv_file']

        if not file.name.endswith(".csv"):
            messages.error(request, '파일이 csv 형식이 아닙니다.')
            return redirect('movie_upload_from_csv')

        decoded_file = file.read().decode('utf-8').splitlines()
        rdr = csv.reader(decoded_file)
        info = []
        video_ids = []

        for idx, row in enumerate(rdr):
            handle, playlistName, playlistURL, genre, country, description = row
            if(idx != 0):
                matches = ["shorts" , "Shorts", "SHORTS", "Membership", "멤버십"]
                if any([x in playlistName for x in matches]):
                    print("This contains shorts or membership")
                    continue
                else:
                    tuple = (handle, playlistName, playlistURL ,genre, country, description)
                    info.append(tuple)
                    video_ids.append(playlistURL.split("&list=")[0].split("watch?v=")[1])
        file.close()

        instances = []
        movie_to_gerne = []
        # del info[0]
        # print(video_ids)

        data = get_video_details(video_ids)
        # print(data['items'])

        for idx, youtube  in enumerate(data):
            publishedAt = youtube['snippet']['publishedAt']
            publishedAt = datetime.strptime(publishedAt, '%Y-%m-%dT%H:%M:%SZ')
            description = youtube['snippet']['description']
            playlistName = info[idx][1]
            channel = Channel.objects.filter(handle=info[idx][0]).first()
            genre = Genre.objects.filter(name=info[idx][3]).first()
            country = Country.objects.filter(name=info[idx][4]).first()
            playlist = info[idx][2].split("&list=")[1].split("&pp=iAQB")[0]
            trailer = info[idx][2].split("&list=")[0].split("watch?v=")[1]
            poster_image = f"https://img.youtube.com/vi/{trailer}/mqdefault.jpg"
            
            # Add logic to upload episodes.
            episodeData = get_playlist_info(playlist)

            try:
                new_movie = Movie.objects.get(title=playlistName, trailer=trailer, playlist=playlist)
                print("movie already exists")                
            # instances.append(Movie(title=playlistName, trailer=trailer, playlist=playlist, poster_image=poster_image, channel=channel, release_date=publishedAt, description=description))
            except Movie.DoesNotExist:
                new_movie = Movie.objects.create(title=playlistName, trailer=trailer, playlist=playlist, poster_image=poster_image, channel=channel, release_date=publishedAt, description=description)
                new_id = new_movie.pk
                new_movie.genre.through.objects.update_or_create(movie_id=new_id, genre_id=genre.pk)
                new_movie.country.through.objects.update_or_create(movie_id=new_id, country_id=country.pk)

                for episode in episodeData['items']:
                    episodeTitle = episode['snippet']['title']
                    episodeId = episode['snippet']['resourceId']['videoId']
                    episodePublishedAt = episode['snippet']['publishedAt']
                    episodePublishedAt = datetime.strptime(episodePublishedAt, '%Y-%m-%dT%H:%M:%SZ')
                    episodeDescription = episode['snippet']['description']

                    episodeDetails = get_video_details([episodeId])
                    print(len(episodeDetails))
                    if (len(episodeDetails) == 0):
                        episodeViewCount = 0
                        episodeLikeCount = 0
                        episodeCommentCount = 0
                        episodeDuration = 0
                    else:
                        try:
                            episodeViewCount = episodeDetails[0]['statistics']['viewCount']
                            episodeLikeCount = episodeDetails[0]['statistics']['likeCount']
                            episodeCommentCount = episodeDetails[0]['statistics']['commentCount']
                            episodeDuration = episodeDetails[0]['contentDetails']['duration']
                        except:
                            episodeViewCount = 0
                            episodeLikeCount = 0
                            episodeCommentCount = 0
                    # episodeComments = get_comments(episodeId)

                    # try:
                    #     episodeComments = episodeComments['items']
                    # except :
                    #     episodeComments = []
                    try:
                        highlight = get_highlights([episodeId])[0]['mostReplayed']
                        episodeHighlights = {"start": highlight['heatMarkersDecorations'][0]['timedMarkerDecorationRenderer']['visibleTimeRangeStartMillis'], "end":highlight['heatMarkersDecorations'][0]['timedMarkerDecorationRenderer']['visibleTimeRangeEndMillis']}
                    except :
                        episodeHighlights = {"start":0, "end":5000}

                    try:
                        new_episode = Episode.objects.get(name=episodeTitle, link=episodeId)
                        print("episode already exists")
                    except:
                        new_episode = Episode.objects.create(name=episodeTitle, description=episodeDescription, 
                        link=episodeId, release_date=episodePublishedAt,
                        viewCount=episodeViewCount, likeCount=episodeLikeCount, commentCount=episodeCommentCount, 
                        duration=episodeDuration, highlights=episodeHighlights)

                        new_movie.episode.through.objects.update_or_create(movie_id=new_id, episode_id=new_episode.pk)



            except IntegrityError:
                messages.error(request, '등록된 플레이리스트와 중복된 정보가 있습니다.')
                return redirect('movie_upload_from_csv')
            # try:
            #     Movie.objects.bulk_create(instances)
            #     Movie.tags.through.objects.bulk_create(movie_to_gerne)
            # except IntegrityError:
            #     messages.error(request, '등록된 플레이리스트와 중복된 정보가 있습니다.')
            #     return redirect('movie_upload_from_csv')
        else:
            messages.info(request,"성공적으로 등록되었습니다.")
            return redirect("playlist_list")
        
def episode_upload_from_csv(request):
    if request.method == "GET":
        return render(request,'episode_upload_csv.html')
    if request.method == "POST":
        file = request.FILES['csv_file']

        if not file.name.endswith(".csv"):
            messages.error(request, '파일이 csv 형식이 아닙니다.')
            return redirect('episode_upload_from_csv')

        decoded_file = file.read().decode('utf-8').splitlines()
        rdr = csv.reader(decoded_file)
        info = []

        for row in rdr:
            name, email = row
            tuple = (name, email)
            info.append(tuple)
        file.close()

        instances = []
        for (name, email) in info:
            instances.append(Movie(full_name=name, email=email, status="수강생"))

        try:
            Movie.objects.bulk_create(instances)
        except IntegrityError:
            messages.error(request, '등록된 유저와 중복된 정보가 있습니다.')
            return redirect('episode_upload_from_csv')
        else:
            messages.info(request,"성공적으로 등록되었습니다.")
            return redirect("member_list")
        


class LatestRateView(View):
    def get(self, request):
        latest_ratings = Rating.objects.all().order_by('-id')[:10]
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
        }for rating in latest_ratings]

        return JsonResponse({"result" :comment_list}, status=200)

# Get list of movies by it's wantu_score
class RankingView(View):
    @method_decorator(cache_page(60*60*24))
    def get(self, request):
        search = request.GET.get('search', '')
        country_name  = request.GET.get("country")
        genre1        = request.GET.get("genre1")
        genre2        = request.GET.get("genre2")
        rating        = request.GET.get("rating","")
        KOREAN_MOVIE  = "한국"
        FOREIGN_MOVIE = "외국"
        LIMIT         = 25
        OFFSET        = 0

        q = Q()
        
        if country_name == KOREAN_MOVIE:
            q.add(Q(country__name=KOREAN_MOVIE), q.AND)

        if country_name == FOREIGN_MOVIE:
            q.add(~Q(country__name=KOREAN_MOVIE), q.AND)

        if genre1 or genre2:
            q.add(Q(genre__name=genre1)|Q(genre__name=genre2), q.AND)

        movies = Movie.objects.filter(q).order_by('-wantu_score').distinct()
        movie_list = [{
            "country_name"   : [country.name for country in movie.country.all()],
            "movie_name"     : movie.title,
            "movie_id"       : movie.id,
            "total_views"     : movie.total_views,
            "total_likes"     : movie.total_likes,
            "total_comments"  : movie.total_comments,
            "total_episodes"  : movie.total_videos,
            "total_videos" : movie.total_videos,
            "wantu_score" : movie.wantu_score,
            "is_new" : movie.is_new,
            "released_date"  : movie.release_date,
            "average_rating" : movie.average_rating,
            "poster_image"   : movie.poster_image,
            "trailer"        : movie.trailer,
            "genres"         : [genre.name for genre in movie.genre.all()],
        } for movie in movies][OFFSET : LIMIT]

        return JsonResponse({"results" : movie_list}, status=200)
    
class PlayHistoryView(View):
    @login_decorator
    def post(self, request,movie_id):
        try:
            user_id = request.user.id
            print("user_id",user_id)
            # get data from request
            data = json.loads(request.body)
            print(data)
            episodeLink = data['episode']
            episode = Episode.objects.get(link=episodeLink)
            play_history = PlayHistory.objects.get(user_id=user_id, movie_id=movie_id)
            play_history.episode=episode
            play_history.last_played=datetime.now()
            play_history.save()
            print("HISTORY UPDATED")
            return JsonResponse({"MESSAGE" : "UPDATED"}, status=200)
        except PlayHistory.DoesNotExist:
                print("Added to history")
                PlayHistory.objects.create(user_id=user_id, movie_id=movie_id, episode=episode)
                return JsonResponse({"MESSAGE" : "CREATED"}, status=200)

        except ValueError:
                return JsonResponse({"MESSAGE" : "VALUE_ERROR"}, status=404)
        except KeyError:
                return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=404)

    @login_decorator
    def get(self, request, movie_id):
        print("History called")
        try:
            user_id = request.user.id
            print("user_id",user_id)
            play_history = PlayHistory.objects.get(user_id=user_id, movie_id=movie_id)
            print("Playlist exist!")
            play_history_info = {
                "episode" : play_history.episode.name,
                "episode_id" : play_history.episode.link,
                "last_played" : play_history.last_played
            }
            print(play_history_info)
            return JsonResponse({"play_history_info" : play_history_info}, status=200)
        except PlayHistory.DoesNotExist:
            print("no history found...")
            play_history_info = {
                "episode" : None,
                "episode_id" : None,
                "last_played" : None
            }

            return JsonResponse({"play_history_info" : play_history_info}, status=200)

class MainTopRankView(View):
    # @method_decorator(cache_page(60*60*1))
    def get(self, request):
        try:
            genres = Genre.objects.all()
            result = []

            for genre in genres:
                movies = Movie.objects.filter(genre=genre).order_by('-wantu_score')[:20]
                movie_list = [{
                    "country_name"   : [country.name for country in movie.country.all()],
                    "movie_name"     : movie.title,
                    "movie_id"       : movie.id,
                    "total_views"     : movie.total_views,
                    "total_likes"     : movie.total_likes,
                    "total_comments"  : movie.total_comments,
                    "total_episodes"  : movie.total_videos,
                    "total_videos" : movie.total_videos,
                    "wantu_score" : movie.wantu_score,
                    "is_new" : movie.is_new,
                    "released_date"  : movie.release_date,
                    "average_rating" : movie.average_rating,
                    "poster_image"   : movie.poster_image,
                    "trailer"        : movie.trailer,
                    "genres"         : [genre.name for genre in movie.genre.all()],
                } for movie in movies]

                result.append({
                    "genre": genre.name,
                    "top_movies": movie_list
                })

            recently_added = Movie.objects.order_by('-last_updated')[:10]
            recently_added_list = [{
                "country_name"   : [country.name for country in movie.country.all()],
                "movie_name"     : movie.title,
                "movie_id"       : movie.id,
                "total_views"     : movie.total_views,
                "total_likes"     : movie.total_likes,
                "total_comments"  : movie.total_comments,
                "total_episodes"  : movie.total_videos,
                "total_videos" : movie.total_videos,
                "wantu_score" : movie.wantu_score,
                "is_new" : movie.is_new,
                "released_date"  : movie.release_date,
                "average_rating" : movie.average_rating,
                "poster_image"   : movie.poster_image,
                "trailer"        : movie.trailer,
                "genres"         : [genre.name for genre in movie.genre.all()],
            } for movie in recently_added]

            result.append({
                "recently_added": recently_added_list
            })

            top_rated = Movie.objects.order_by('-wantu_score')[:10]
            top_rated_list = [{
                "country_name"   : [country.name for country in movie.country.all()],
                "movie_name"     : movie.title,
                "movie_id"       : movie.id,
                "total_views"     : movie.total_views,
                "total_likes"     : movie.total_likes,
                "total_comments"  : movie.total_comments,
                "total_episodes"  : movie.total_videos,
                "total_videos" : movie.total_videos,
                "wantu_score" : movie.wantu_score,
                "is_new" : movie.is_new,
                "released_date"  : movie.release_date,
                "average_rating" : movie.average_rating,
                "poster_image"   : movie.poster_image,
                "trailer"        : movie.trailer,
                "genres"         : [genre.name for genre in movie.genre.all()],
            } for movie in top_rated]

            result.append({
                "top_rated": top_rated_list
            })


            return JsonResponse({"result": result}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
