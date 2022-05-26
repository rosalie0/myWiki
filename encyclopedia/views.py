from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from markdown2 import Markdown
markdowner = Markdown()

from . import util
import encyclopedia

import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def getEntry(request, name):
    # get_entry returns None if the entry does not exist in our list of entries
    if util.get_entry(name) == None:
        return render(request, "encyclopedia/notfound.html", {
            "name": name
        })

    # If it does exist, convert .md to html and return the page
    else:
        page = util.get_entry(name) # page is an .md file of entry name
        convertedPage = markdowner.convert(page) # md->html

        return render(request, "encyclopedia/entry.html", {
            "page": convertedPage,
            "name": name,
        })



def create(request):
    if request.method == "POST":
        name = request.POST.get("name")

        # If entry already exists with provided title, user should be presented with an error message.
        if util.get_entry(name):
            messages.error(request, f'Creation failed: An entry for "{name}" already exists.')
            return render (request, "encyclopedia/create.html", {
                "name": name,
            })
        
        # If the entry is a new entry, save its content, and return that page
        else:
            content = request.POST.get("content")
            util.save_entry(name, content)
            return getEntry(request, name)


    # If GET method, return create page normally.
    else:
        return render(request, "encyclopedia/create.html")



def edit(request, name):
    # If we are recieving form input, save the content and just return that page
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(name, content)
        return getEntry(request, name)

    # If GET method, get entry's markdown content and return it.
    else:
        markdownContent = util.get_entry(name)
        return render(request, "encyclopedia/edit.html", {
            "name": name,
            "markdownContent": markdownContent,
        })


def randomEntry(request):
    entries = util.list_entries()
    entry = random.choice(entries)     # random.choice(items) returns a single random item
    return getEntry(request, entry)   


def search(request):
    query = request.GET.get("q")
    if request.method == "GET":
        
        # results is a list of entries where q is a substring,
        # eg if q="thon" results=["Python", "Python Syntax", "Marathon"]
        results = [] 

        entries = util.list_entries()
        for entry in entries:
            # use .lower() for all strings because we will ignore casing

            # If q is an exact match with an entry, redirect to it.
            if query.lower() == entry.lower():
                return getEntry(request, entry)
            
            # If q is a substring of entry, put entry in results
            elif query.lower() in entry.lower():
                results.append(entry)
        
        return render(request, "encyclopedia/searchresults.html", {
            "query": query,
            "results": results,
        })

    # Returns this if req method isn't get  (Shouldn't hit this??)   
    return HttpResponse("Write later")