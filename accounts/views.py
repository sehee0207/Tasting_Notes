from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from accounts.forms import UserChangeForm


def signup(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('photo:index')
    else:
        form = UserChangeForm()
    return render(request, 'signup.html', {'form': form})