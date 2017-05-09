from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View


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

    @user_passes_test(lambda u: u.is_superuser)
    def delete(self, request):
        User.objects.filter(is_superuser=False).delete()
        return JsonResponse({'result': 'ok'})