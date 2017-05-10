from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from pix.models import Image


def report_error_in_json(f):
    """
    Decorator used to prevent errors to soak down to user as 500 server error.
    """

    def new_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return JsonResponse({'result': str(e)}, status=500)

    return new_f


def login_required(f):
    """
    Custom hardcoded version to prevent anonymous users to use resources that are only for authorized users.
    """
    def new_f(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'result': 'you have to be logged in to perform this action'}, status=401)
        return f(request, *args, **kwargs)
    return new_f


@method_decorator(report_error_in_json, name='dispatch')
class LoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'result': 'ok'})
        else:
            return JsonResponse({'result': 'incorrect username or password'})

    @method_decorator(login_required)
    def delete(self, request):
        logout(request)
        return JsonResponse({'result': 'ok'})


@method_decorator(report_error_in_json, name='dispatch')
class UsersView(View):
    @method_decorator(login_required)
    def get(self, request):
        result = [x.username for x in User.objects.all()]
        return JsonResponse({'result': 'ok', 'users': result})

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        u = User.objects.create_user(username, email, password)
        return JsonResponse({'result': 'ok', 'user': u.get_username()}, status=201)


@method_decorator(report_error_in_json, name='dispatch')
class UserView(View):
    @method_decorator(login_required)
    def get(self, request, username):
        u = User.objects.get(username=username)
        return JsonResponse({
            'username': u.get_username(),
            'email': u.email,
            'likes': sum([len(x.likes.all()) for x in Image.objects.filter(author=u)]),
        })

    @method_decorator(login_required)
    def delete(self, request, username):
        if not (request.user.get_username() == username or request.user.is_superuser):
            return JsonResponse({'result': 'you have no permission to delete %s user' % username}, status=401)
        u = User.objects.get(username=username)
        u.delete()
        return JsonResponse({'result': 'ok'})


@method_decorator(report_error_in_json, name='dispatch')
class ImagesView(View):
    def get(self, request):
        result = {'result': 'ok', 'images': []}
        if request.GET.get('my', None) is not None and request.user.is_authenticated:
            collection = Image.objects.filter(author=request.user)
        elif request.GET.get('popularity', None) is not None:
            collection = Image.objects.all()
            all_likes = 0
            for i in collection:
                all_likes += len(i.likes.all())
            print(all_likes / 10)
            if request.GET['popularity'] == 'main':
                collection = Image.objects.filter(likes__gt=(all_likes / 10.0)).distinct()
            elif request.GET['popularity'] == 'waiting':
                collection = Image.objects.exclude(likes__gte=(all_likes / 10.0)).distinct()
            else:
                return JsonResponse({'result': 'wrong value for "popularity parameter"'})
        else:
            collection = Image.objects.all()

        for i in collection:
            pic = {
                'title': i.title,
                'pk': i.id,
                'url': '/images/%s' % i.id,
                'likes': len(i.likes.all()),
                'user': i.author.get_username(),
            }
            result['images'].append(pic)
        return JsonResponse(result)

    @method_decorator(login_required)
    def post(self, request):
        title = request.POST['title']
        image = request.FILES['image']
        Image.objects.create(title=title, image=image)
        return JsonResponse({'result': 'ok'})


@method_decorator(report_error_in_json, name='dispatch')
class ImageView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        image = Image.objects.get(pk=pk)
        return HttpResponse(image.image, content_type='image/%s' % image.image.name.split('.')[-1])

    @method_decorator(login_required)
    def patch(self, request, pk):
        if request.GET.get('like') is not None:
            image = Image.objects.get(pk=pk)
            user = request.user
            if user in image.likes.all():
                image.likes.remove(user)
            else:
                image.likes.add(user)
            result = {'result': 'ok', 'likes': len(image.likes.all())}
            return JsonResponse(result)
        else:
            return JsonResponse({'result': 'unspecific patch request'})

    @method_decorator(login_required)
    def delete(self, request, pk):
        image = Image.objects.get(pk=pk)
        if image.author != request.user and not request.user.is_superuser:
            return JsonResponse({'result': 'you have no permission to delete this resource'})
        image.delete()
        return JsonResponse({'result': 'ok'})
