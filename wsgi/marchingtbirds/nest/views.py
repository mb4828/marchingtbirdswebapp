from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404, get_object_or_404
from forms import RegistrationForm, ProfileForm, PasswordChangeForm
from models import Student, AuthenticationCode, Bulletin

SITE_SUF = ' - Marching Thunderbirds NEST'

def nest_home(request):
    # is the user logged in?
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/nest/login/')
    if request.user.is_staff:
        return HttpResponseRedirect('/admin/')

    # locate student object if it exists
    try:
        student = Student.objects.get(user__pk=request.user.pk)
    except:
        student = ''

    # fetch bulletin list
    bulletins = Bulletin.objects.all().order_by('-last_update')

    context = { 'title':'Dashboard'+SITE_SUF, 'navlight':3, 'request':request, 'user':request.user, 'student':student, 'bulletins':bulletins, }
    return render(request, 'nest/home.html', context)

def profile(request):
    message = ''
    saved = False
    option = request.GET.get('mode')

    # is the user logged in?
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/nest/login/')
    if request.user.is_staff:
        return HttpResponseRedirect('/admin/')

    # locate student object and load its form if it exists
    student = 0
    try:
        student = Student.objects.get(user__pk=request.user.pk)
        form = ProfileForm(instance=student)
    except:
        form = ProfileForm()

    # render depending on what the user asked us to do
    if option == 'view' or not option:
        saved = True
        context = { 'title':'View my profile'+SITE_SUF, 'navlight':3, 'request':request, 'user':request.user, 'form':form, 'view':1, 'message':message, 'saved':saved}
        return render(request, 'nest/profile.html', context)

    elif option == 'edit':
        if request.method == 'POST':
            if student:
                prof_form = ProfileForm(data=request.POST, instance=student)
            else:
                prof_form = ProfileForm(data=request.POST)

            if prof_form.is_valid():
                if student:
                    # user has already been associated with a student
                    student = prof_form.save(commit=False)
                else:
                    # we must now associate the user with the student
                    student = prof_form.save(commit=False)
                    student.user = request.user     # ta da!

                # update our other data and save
                request.user.first_name = student.first_name
                request.user.last_name = student.last_name
                request.user.email = student.student_email
                student.save()
                request.user.save()

                # create a message and redirect to the dashboard
                messages.add_message(request, messages.SUCCESS, "Your profile has been updated")
                return HttpResponseRedirect('/nest/')

            else:
                form = prof_form
                message = '<span style="color:firebrick">Please correct the errors below</span>'
                saved = False

        context = { 'title':'Edit my profile'+SITE_SUF, 'navlight':3, 'request':request, 'user':request.user, 'form':form, 'view':0, 'message':message, 'saved':saved,}
        return render(request, 'nest/profile.html', context)
    else:
        raise Http404

def password_change(request):
    message = ''
    saved = False
    form = PasswordChangeForm()

    # is the user logged in?
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/nest/login/')
    if request.user.is_staff:
        return HttpResponseRedirect('/admin/')

    # change password
    if request.method == 'POST':
        pcform = PasswordChangeForm(data=request.POST)

        if pcform.is_valid():
            # still have to check if old password matches
            u = request.user
            oldpass = request.POST.get('oldpass')
            newpass = request.POST.get('newpass1')

            if u.check_password(oldpass):
                # passwords match so it's safe to change the password
                u.set_password(newpass)
                u.save()

                # for some reason, the user gets logged out so we have to log them in again
                login(request, authenticate(username=u.username, password=newpass))

                # create a message and redirect to the dashboard
                messages.add_message(request, messages.SUCCESS, "Your password has been changed successfully")
                return HttpResponseRedirect('/nest/')

            else:
                form = pcform
                message = '<span style="color:firebrick">Old password is incorrect. Please try again</span>'

        else:
            form = pcform
            message = '<span style="color:firebrick">Please correct the errors below</span>'

    context = { 'title':'Change my password'+SITE_SUF, 'navlight':3, 'request':request, 'message':message, 'form':form, 'saved':saved, }
    return render(request, 'nest/passwordchange.html', context)

def register(request):
    registered = False
    disabled = False

    # is registration disabled?
    if not (AuthenticationCode.objects.all()[0]).enable:
        disabled = True
        context = {'title': 'Create an account' + SITE_SUF, 'navlight':3, 'request':request, 'disabled':disabled,}
        return render(request, 'nest/register.html', context)

    # registration is enabled
    if request.method == 'POST':
        reg_form = RegistrationForm(data=request.POST)

        if reg_form.is_valid():
            reg_form.save(request.POST)     # automatically creates new user & student objects
            registered = True

    else:
        reg_form = RegistrationForm()

    context = {'title': 'Create an account' + SITE_SUF, 'navlight':3, 'request':request, 'reg_form': reg_form, 'registered': registered, 'disabled':disabled,}
    return render(request, 'nest/register.html', context)

def user_login(request):
    error = ''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get('remember', False)

        user = authenticate(username=username, password=password)

        if not remember:
            request.session.set_expiry(0)   # handle do not remember case

        if user:
            if user.is_staff and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/admin/')
            elif user.is_active:
                login(request, user)
                return HttpResponseRedirect('/nest/')
            else:
                error = 'Your NEST account has been disabled. If this is an error, please contact the MTB staff.'
        else:
            error = 'The username or password you entered is incorrect'

    else:
        if request.GET.get('changepass') == '1':
            error = 'Unfortunately, our site does not support password recovery at this time. To recover your password, please contact the MTB staff.'

    context = {'title': 'Login' + SITE_SUF, 'navlight':3, 'request':request, 'error':error,}
    return render(request, 'nest/login.html', context)

def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "You have been logged out")
    return HttpResponseRedirect('/')

def privacy(request):
    context = {'title': 'Privacy Policy' + SITE_SUF, 'request':request,}
    return render(request, 'nest/privacy.html', context)

def uniform(request):
    """
    No longer used because the uniform page was depreciated when the new dashboard was built. Left just in case.
    """
    message = ''
    tshirt = ''
    student = 0

    # is the user logged in?
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/nest/login/')
    if request.user.is_staff:
        return HttpResponseRedirect('/admin/')

    # locate student object if it exists
    try:
        student = Student.objects.get(user__pk=request.user.pk)
    except:
        message = 'Please complete your profile in order to view uniform assignments.'

    try:
        tshirt = student.TSHIRT_SIZES[student.tshirt-1][1]
    except:
        tshirt = 'None'

    context = { 'title':'View my uniform'+SITE_SUF, 'navlight':3, 'request':request, 'student':student, 'tshirt':tshirt, 'message':message, }
    return render(request, 'nest/uniform.html', context)