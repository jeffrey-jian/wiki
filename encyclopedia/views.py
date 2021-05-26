from django import forms
from django.shortcuts import render, redirect
import markdown2
import random

from . import util

# Form to create new wiki page
class CreatePageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Markdown Content", widget=forms.Textarea)

# Form for editing page
class EditPageForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea)
    

def entry(request, item):
    # error if page doesn't exist
    if util.get_entry(item) == None:
        return render(request, "encyclopedia/error.html", {
            "item": item
        })
    # load page with title and content
    return render(request, "encyclopedia/item.html", {
    "content": markdown2.markdown(util.get_entry(item)),
    "item": item
    })
 

def search(request):
    if request.method == "POST":
        item = request.POST.get('q')
        if  util.get_entry(item):
            return render(request, "encyclopedia/item.html", {
            "content": markdown2.markdown(util.get_entry(item)),
            "item": item
            })
        else:
            matches = []
            entries = util.list_entries()
            for entry in entries:
                if item.lower() in entry.lower():
                    matches.append(entry)
            return render(request, "encyclopedia/search.html", {
                "matches": matches,
                "item": item
            })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def newpage(request):
    
    valid = True
    duplicate = False
    
    if request.method == "POST":
        # pull form input
        form = CreatePageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            content = "#" + title + "\n \n" + content 
            print(title)
            print("............................................")
            print(content)
            # check if page with same title exists
            if util.get_entry(title) == None:
                util.save_entry(title, content)
                return entry(request, title)
            else:
                duplicate = True
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "duplicate": duplicate,
                    "title": title
                })
        # if form input is invalid
        else:
            valid = False
            return render(request, "encyclopedia/newpage.html", {
                "form": form,
                "valid": valid
            })

    return render(request, "encyclopedia/newpage.html", {
        "form": CreatePageForm
    })

def editpage(request, item):
    valid = True
    if request.method == "POST":
        # pull form input
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(item, content)
            return entry(request, item)
        # if form input is invalid
        else:
            valid = False
            return render(request, "encyclopedia/editpage.html", {
                "form": form,
                "valid": valid
            })

    raw_content = util.get_entry(item)
    form = EditPageForm({"content": raw_content})
    return render(request, "encyclopedia/editpage.html", {
        "form": form,
        "title": item
    })

def randompage(request):
    entries = util.list_entries()
    length = len(entries)
    num = random.randint(0, length - 1)
    entry = entries[num]
    return render(request, "encyclopedia/item.html", {
        "item": entry,
        "content": markdown2.markdown(util.get_entry(entry))
    })

