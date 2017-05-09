from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from pix.models import PixUser


class UsersView(View):
    @method_decorator(login_required)
    def get(self, request):
        result = [x.username for x in User.objects.all()]
        return JsonResponse({'result': 'ok', 'users': result})

    def post(self, request):
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            u = User.objects.create_user(username, email, password)
            u.is_active = False
            u.save()
            return JsonResponse({'result': 'ok'}, status=201)
        except Exception as e:
            return JsonResponse({'result': str(e)}, status=500)

            # @user_passes_test(lambda u: u.is_superuser)
            # def delete(self, request):
            #     User.objects.filter(is_superuser=False).delete()
            #     return JsonResponse({'result': 'ok'})


class UserView(View):
    @method_decorator(login_required)
    def get(self, request, username):
        u = PixUser.objects.get(user__username__exact=username)
        if u is None:
            return JsonResponse({'result': 'no such user found'}, status=404)
        return JsonResponse({
            'username': u.get_username(),
            'pluses': sum([len(x.pluses) for x in u.pictures]),
        })

    @method_decorator(login_required)
    def delete(self, request, username):
        if not (request.user.get_username() == username or request.user.is_superuser):
            return JsonResponse({'result': 'you have no permission to delete %s user' % username}, status=401)
        u = PixUser.objects.get(username=username)
        u.delete()
        return JsonResponse({'result': 'ok'})


class ImagesView(View):
    @method_decorator(login_required)
    def get(self, request):
        pass

    @method_decorator(login_required)
    def post(self, request):
        pass


class ImageView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        pass

    @method_decorator(login_required)
    def delete(self, request, id):
        pass
