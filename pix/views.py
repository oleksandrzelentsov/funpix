from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
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


def register_test(request):
    template_name = 'user_register_test.html'
    return render(request, template_name)


def index(request):
    template_name = 'home.html'
    return render(request, template_name)


def is_user_authenticated(request):
    if request.user.is_authenticated:
        return JsonResponse({'result': 'ok'})
    else:
        return JsonResponse({'result': 'user is not authenticated'})


def get_raw_image(request, pk):
    image = Image.objects.get(pk=pk)
    return HttpResponse(image.image, content_type='image/%s' % image.image.name.split('.')[-1])


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
        u = User.objects.create_user(username, email, password, is_active=False)
        return JsonResponse({'result': 'ok', 'user': u.get_username()}, status=201)

    # @user_passes_test(lambda u: u.is_superuser)
    # def delete(self, request):
    #     User.objects.filter(is_superuser=False).delete()
    #     return JsonResponse({'result': 'ok'})


@method_decorator(report_error_in_json, name='dispatch')
class UserView(View):
    @method_decorator(login_required)
    def get(self, request, username):
        u = User.objects.get(username=username)
        return JsonResponse({
            'username': u.get_username(),
            'likes': sum([x.likes for x in u.images.all()]),
            'liked': len(u.likes.all()),
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
    # @method_decorator(login_required)
    def get(self, request):
        result = {'result': 'ok', 'images': []}
        for i in Image.objects.all():
            pic = {
                'title': i.title,
                'url': '/raw/images/%s' % i.id,
                'likes': i.likes
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
    def get(self, request, id):
        pass

    @method_decorator(login_required)
    def delete(self, request, id):
        pass
