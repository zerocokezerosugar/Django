from django.shortcuts import redirect, render
from .models import Topic,Choice
# Create your views here.
def index(request):
    t = Topic.objects.all()
    t = t.order_by("-pubdate")
    context={
        "tset":t
    }
    return render(request,"vote/index.html",context)

def detail(request,vpk):
    t = Topic.objects.get(id=vpk)
    cho = t.choice_set.all()
    context = {
        't':t,
        "cset":cho
    }
    return render(request,'vote/detail.html',context)

def del_u(request,vpk):
    t = Topic.objects.get(id = vpk)
    if request.user == t.maker:
        t.delete()
    return redirect('vote:index')

def vote(request,vpk):
    t = Topic.objects.get(id = vpk)
    if not request.user in t.voter.all(): #투표자에 유저가 없다면 추가하고 있으면 추가안함
        t.voter.add(request.user)

        cpk = request.POST.get("ch")
        c = Choice.objects.get(id = cpk)
        c.choicer.add(request.user)

    return redirect('vote:detail',vpk)

def cancel(request,vpk):
    t = Topic.objects.get(id= vpk)
    u = request.user
    if u in t.voter.all():
        t.voter.remove(u)
        u.choice_set.get(topic = t).choicer.remove(u) 
        #유저가 고른것중에 가져와라 topic이 t인것을 , u가 투표한 초이스 레코드
    return redirect('vote:detail',vpk)

from django.utils import timezone
def create(request):
    if request.method =="POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        
        names = request.POST.getlist("chname")       
        files = request.FILES.getlist("pic")
        cons = request.POST.getlist("chcon")
        
        t = Topic(subject = s, maker = request.user, content = c, pubdate=timezone.now())
        t.save()
        if len(names)>1:
            for i,j,k in zip(names, files, cons):
                c = Choice(topic = t, chname = i, chpic = j, chcom = k)
                print(c)
                c.save()
            return redirect('vote:index')
        else:
            return redirect('vote:create')

    return render(request, 'vote/create.html')