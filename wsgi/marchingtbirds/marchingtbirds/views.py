from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from marchingtbirds.models import NewsPost, StaffMember, HistoryRecord, CurrentFieldShow, CoverPhoto

SITE_SUF = ' - Mahwah Marching Thunderbirds'


def home(request):
    # news posts
    try:
        post_list = NewsPost.objects.all().order_by('-pub_date')[:5]
        more_flag = NewsPost.objects.count() > 5
    except:
        post_list = ''
        more_flag = ''

    # cover photo
    cp = 0
    try:
        photos = CoverPhoto.objects.all().order_by('-last_update')

        if photos:
            for p in photos:
                if p.display:
                    cp = p
                    break
    except:
        photos = ''

    desc = 'The official website of the Mahwah Marching Thunderbirds, the marching band of Mahwah High School, NJ.'
    nl = 0
    context = {'title': 'Mahwah Marching Thunderbirds', 'description': desc, 'post_list': post_list, 'more': more_flag, 'cover': cp, 'navlight': nl, 'request':request }
    return render(request, 'marchingtbirds/home.html', context)

def morenews(request):
    entry_list = NewsPost.objects.all().order_by('-pub_date')
    p = Paginator(entry_list, 10)    # show 10 entries per page

    page = request.GET.get('page')
    try:
        post_list = p.page(page)
    except PageNotAnInteger:
        # deliver first page
        post_list = p.page(1)
    except EmptyPage:
        # deliver last page
        post_list = p.page(p.num_pages)

    context = {'title': 'News Archive'+SITE_SUF, 'post_list': post_list, 'request': request }
    return render(request, 'marchingtbirds/morenews.html', context)

def detail(request, url):
    try:
        entries = NewsPost.objects.all()
        for entry in entries:
            if entry.getUrl() == url:
                context = { 'title':entry.title, 'entry':entry, 'request':request }
                return render(request, 'marchingtbirds/detail.html', context)
    except NewsPost.DoesNotExist:
        raise Http404

    raise Http404

def staff(request):
    desc = 'To contact a member of the Marching Thunderbirds staff, click the "send a message" link below their name.'
    nl = 1
    entries = StaffMember.objects.all().order_by('order')
    context = { 'title':'Staff'+SITE_SUF, 'description':desc, 'navlight':nl, 'request':request, 'page_title':'Staff', 'entries':entries }
    return render(request, 'marchingtbirds/staffhist.html', context)

def hist(request):
    entry_list = HistoryRecord.objects.all().order_by('-year')
    p = Paginator(entry_list, 8)    # show 8 entries per page

    page = request.GET.get('page')
    try:
        entry_list = p.page(page)
    except PageNotAnInteger:
        # deliver first page
        entry_list = p.page(1)
    except EmptyPage:
        # deliver last page
        entry_list = p.page(p.num_pages)

    desc = 'Past field shows, videos, and multimedia presentations from previous seasons.'
    nl = 1
    #entries = HistoryRecord.objects.all().order_by('-year')
    context = { 'title':'History'+SITE_SUF, 'description':desc, 'navlight':nl, 'request':request, 'page_title':'History', 'entries':entry_list }
    return render(request, 'marchingtbirds/staffhist.html', context)

def tradition(request):
    desc = "Our organization's mission and philosophy."
    nl = 1
    context = { 'title':'Tradition & Philosophy'+SITE_SUF, 'description':desc, 'navlight':nl, 'request':request }
    return render(request, 'marchingtbirds/tradition.html', context)

def faq(request):
    desc = 'Common questions asked by new and potential band members about what its like to be part of our program.'
    nl = 2
    context = { 'title':'Marching Band FAQs'+SITE_SUF, 'description':desc, 'navlight':nl, 'request':request }
    return render(request, 'marchingtbirds/faq.html', context)

def bandcamp(request):
    desc = 'Is band camp really like its portrayed in the movies? Not at all!'
    nl = 2
    context = { 'title':'About Band Camp'+SITE_SUF, 'description':desc, 'navlight':nl, 'request':request }
    return render(request, 'marchingtbirds/bandcamp.html', context)

def fieldshow(request):
    desc = 'Information about the current field show and links to audio files for students to practice with.'
    nl = 3

    entries = CurrentFieldShow.objects.all().order_by('-year')
    entry = 0

    if entries:
        for e in entries:
            if e.display:
                entry = e
                break

    context = { 'title':'Current Field Show'+SITE_SUF, 'description':desc, 'navlight':nl, 'request':request, 'show':entry }
    return render(request, 'marchingtbirds/fieldshow.html', context)

def calendar(request):
    desc = 'Our full-season calendar, including all performances, parades, competitions, and other events.'
    nl = 3
    context = { 'title':'Full Season Calendar'+SITE_SUF, 'description':desc, 'navlight':nl, 'request':request }
    return render(request, 'marchingtbirds/calendar.html', context)

def memorialday(request):
    desc = 'Music and audio files for the annual Mahwah Memorial Day Parade.'
    nl = 3
    context = { 'title':'Memorial Day'+SITE_SUF, 'description':desc, 'navlight':nl, 'request':request }
    return render(request, 'marchingtbirds/memorialday.html', context)