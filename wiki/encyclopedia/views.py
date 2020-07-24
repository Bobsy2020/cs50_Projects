from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render
import markdown2
from markdown2 import Markdown
#Import os module
import os
import random
from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):

    markdown_text = util.get_entry(title)
    html = markdown2.markdown(markdown_text)
    return render(request, "encyclopedia/wiki.html", {
        "text":html,
        "title":title
    })

def search(request):
    search_string = request.GET.get('q', '')
    titles = util.list_entries()
    if search_string:
        searchResult = []
        for title in titles:
            if search_string == title:
                markdown_text = util.get_entry(title)
                html = markdown2.markdown(markdown_text)
                return render(request, "encyclopedia/wiki.html", {
                    "text":html,
                    "title":title
                })
            elif search_string.upper() in title.upper():
                searchResult.append(title)
        return render(request, "encyclopedia/search.html", {
               "queryon": search_string,
               "titles": searchResult
                })

def new(request, method = "POST"):

    if request.method == "POST":
        newTitle = request.POST.get("title")
        text = request.POST.get("text")
        # print(newTitle)
        # print(text)
        # check that a title is present
        if not newTitle:
            message = "Title is missing!"
            alert = "alert alert-warning"
            return render(request,"encyclopedia/new.html", {
                    "message": message,
                    "alert": alert,
                    "text": text,
                    "autofocusTitle": "autofocus"
                })
        # check that a description is present        
        elif not text:
            message = "Need a description!"
            alert = "alert alert-warning"
            return render(request,"encyclopedia/new.html", {
                    "message": message,
                    "alert": alert,
                    "title": newTitle,
                    "autofocusText": "autofocus"
                })
        # find out if file already exists
        titles = util.list_entries()
        for title in titles:
            if newTitle == title:
                message = "Title " + title + " already exists!"
                alert = "alert alert-warning"
                #print("title already exists")
                return render(request,"encyclopedia/new.html", {
                    "message": message,
                    "alert": alert,
                    "text": text,
                    "title":title,
                    "autofocusTitle": "autofocus"
                })
            
        # create a new file
        # Create a Python file object using open() and the with statement
        fileName = newTitle + ".md"
        text = "# " + newTitle + "\n\n" + text
        
        with open('entries/' + fileName, 'w') as f:
            myfile = File(f)
            myfile.write(text)
            myfile.closed
        f.closed

        #util.save_entry(newTitle, text)
        markdown_text = util.get_entry(newTitle)
        html = markdown2.markdown(markdown_text)
        return render(request, "encyclopedia/wiki.html", {
            "text":html,
            "title":newTitle
        })
    else:
        # print("GET request")
        message = "Please enter a title and description."
        alert = "alert alert-secondary"
        return render(request,"encyclopedia/new.html", {
            "message": message,
            "alert": alert
        })

def edit(request, title, method="POST"):
    if request.method == "POST":
        text = request.POST.get("text")
        util.save_entry(title, text)
        markdown_text = util.get_entry(title)
        html = markdown2.markdown(markdown_text)
        return render(request, "encyclopedia/wiki.html", {
            "text":html,
            "title":title
        })

    else:
        markdown_text = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title":title,
            "text":markdown_text
        })

def randomChoice(request):
    entries = util.list_entries()
    try:
        title=random.choice(entries)
        #return HttpResponse(title)
        markdown_text = util.get_entry(title)
        html = markdown2.markdown(markdown_text)
        return render(request, "encyclopedia/wiki.html", {
            "text":html,
            "title":title
        })   
    except IndexError:
        return HttpResponse("There are no entries!")