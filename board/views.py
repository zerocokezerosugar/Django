
from multiprocessing import context
from django.shortcuts import redirect, render
import googletrans
from .models import Board, Reply
# Create your views here.
from django.core.paginator import Paginator
from django.contrib import messages

def index(request):
    pg = request.GET.get('page',1)
    cate = request.GET.get("cate","")
    kw = request.GET.get("kw","")

    if kw:#키워드가있을때
        if cate == "sub":
            b = Board.objects.filter(subject__contains=kw)
        elif cate == "wri":
            from acc.models import User
            try:
                u = User.objects.get(username = kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
        else:
            b = Board.objects.all()
    else:
        b = Board.objects.all()

    b = b.order_by("-pubdatd")
    pag = Paginator(b, 10)
    obj = pag.get_page(pg)
    context = {
        "bset" : obj,
        "cate" : cate,
        "kw" : kw
    }
    return render(request,"board/index.html",context)

from googletrans import Translator


def trans(request):
    context = {"ndict": googletrans.LANGUAGES}

    if request.method == "POST":
        text = request.POST.get("bf")
        fr = request.POST.get("fr")
        to = request.POST.get("to")
        translator = Translator()
        
        if text:
            inter = translator.translate(text, src=fr , dest=to)
        
            context.update({
                'af':inter.text,
                'text' : text,
                'fr' : fr,
                'to' : to,
            })
        
    return render(request, 'board/trans.html',context)

def detail(request,bpk):
    a = Board.objects.get(id = bpk)
    r = a.reply_set.all()
    context = {
        'a' : a,
        "rset":r
    }
    return render(request,"board/detail.html", context)

def creply(request,bpk):
    c = request.POST.get("com")
    b = Board.objects.get(id=bpk)
    Reply(b = b, replyer = request.user, comment = c, pubdate = timezone.now()).save()
    return redirect("board:detail",bpk)

def delete_con(request,bpk):
    a = Board.objects.get(id = bpk)
    if request.user == a.writer:
        a.delete()
    else:
        messages.info(request,"삭제할수없는 글입니다")
    return redirect("board:index")

def delete_reply(request,bpk,ipk):
    a = Reply.objects.get(id = ipk)
    if request.user == a.replyer:
        a.delete()
        messages.info(request,"삭제했습니다.")
    # else:
    #     pass#안내메세지 
    return redirect("board:index")

from django.utils import timezone
def create(request):
    if request.method == "POST":
        # print(request.POST)
        s = request.POST.get("bsub")
        c = request.POST.get("bcon")
        if s and c:
            Board(subject = s, content = c, writer=request.user, pubdatd=timezone.now()).save()
        # try:          
        #     Board(subject = s, content = c,pubdate=timezone()).save()
        # except:
        #     pass
        return redirect("board:index")
    return render(request,"board/create.html")

def update(request,bpk):   
    b = Board.objects.get(id = bpk)
    context = {
        'b':b
    }
    if request.user == b.writer:
        #19일차 메세지
        return redirect("board:index")

    if request.method == "POST":    
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect('board:detail',bpk)
    return render(request,'board/update.html',context)

def likey(request,bpk):
    b = Board.objects.get(id = bpk)
    b.likey.add(request.user)
    return redirect("board:detail",bpk)

def bad(request,bpk):
    b = Board.objects.get(id = bpk)
    b.likey.remove(request.user)
    return redirect('board:detail',bpk)

