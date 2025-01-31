from django.conf import settings
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login, login
from django.views.generic import FormView

from member.forms import SignupForm, LoginForm
from todo.models import User
from utils.email import send_email


class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    # success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        # return HttpResponseRedirect(self.get_success_url())

        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)
        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/verify/?code={signer_dump}'
        # if settings.DEBUG:  # 디버그 모드일경우 콘솔에 출력 아닐경우 이메일 발송
        #     print(url)
        # else:
        subject = '이메일 인증을 완료해주세요'
        message = f'다음 링크를 클릭해주세요 <br><a href="{url}">{url}</a>'

        send_email(subject, message,  [user.email])


        return render(self.request, template_name='signup_done.html', context={'user': user})

def verify_email(request):
    code = request.GET.get('code', '')
    signer = TimestampSigner()
    try:
        decoded_user_email = signing.loads(code)
        email = signer.unsign(decoded_user_email, max_age = 1800)
    except (TypeError, SignatureExpired):
        return render(request,'not_verified.html')

    user = get_object_or_404(User, email=email, is_active=False)
    user.is_active = True
    user.save()
    login(request, user)
    return render(request,'email_verified_done.html')



class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("todo:list")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user=user)
        return HttpResponseRedirect(self.get_success_url())
