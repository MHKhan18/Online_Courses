from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from django import forms

from . import util

import markdown2

from random import randint 




class SearchForm(forms.Form):
    query = forms.CharField(label="", widget = forms.TextInput(attrs={
        "class" : "search", "placeholder":"Search Encyclopedia"
    }))


class ContentForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(
        label = "Enter content (in markdown format)",
        widget = forms.Textarea)

class EditForm(forms.Form):
    content = forms.CharField(label="", widget = forms.Textarea)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_bar": SearchForm(),
        "heading" : "All pages",
    })

def get_entry(request , title):
    entry = util.get_entry(title)
    available = not entry is None
    html = markdown2.markdown(entry) if available else None
    
    return render(request, "encyclopedia/entry.html", {
        "available": available,
        "title": title,
        "content": html,
        "search_bar": SearchForm(),
    })

def search(request):
    search_bar = SearchForm(request.POST)
    if search_bar.is_valid(): # only respond when there is an input
        query = search_bar.cleaned_data["query"]
        entries = util.list_entries()
        if query in entries: # exact match
            url = reverse("page" , kwargs = {"title" : query})
            return HttpResponseRedirect(url)
       
        possibles = []
        for entry in entries:
            if query.lower() in entry.lower():
                possibles.append(entry)
        
        return render(request, "encyclopedia/index.html", {
            "entries": possibles,
            "search_bar": search_bar,
            "heading" : "Results page",
        })

def create(request):
    if request.method == "POST":
        form = ContentForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html",{
                    "search_bar": SearchForm(),
                    "title" : title,
                })
            else:
                util.save_entry(title, content)
                content = markdown2.markdown(content)
                return render(request, "encyclopedia/entry.html", {
                    "available": True,
                    "title": title,
                    "content": content,
                    "search_bar": SearchForm(),
                })
        else:
            return render(request, "encyclopedia/content.html", {
                "title": "Add Page",
                "search_bar": SearchForm(),
                "heading" : "Create New Page",
                "content" : form,
            })
            
    else: # GET route
        return render(request, "encyclopedia/content.html", {
                "title": "Add Page",
                "search_bar": SearchForm(),
                "heading" : "Create New Page",
                "content" : ContentForm(),
            })
    

def edit(request , title):
    if not title in util.list_entries():
        return render(request, "encyclopedia/error.html",{
                    "search_bar": SearchForm(),
                    "title" : title,
                })

    content = util.get_entry(title)
    form = EditForm({"content" : content}) # bound data

    if request.method == "POST":
        edit_form = EditForm(request.POST)
        if edit_form.is_valid():
            edit_content = edit_form.cleaned_data["content"]
            util.save_entry(title , edit_content)
            url = reverse("page" , kwargs = {"title" : title})
            return HttpResponseRedirect(url)
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "title": title,
                "search_bar": SearchForm(),
                "form" : edit_form,
            })



    # GET
    return render(request, "encyclopedia/edit_page.html", {
                "title": title,
                "search_bar": SearchForm(),
                "form" : form,
            })
    
def random(request):
    entries = util.list_entries()
    num_entries = len(entries)
    index = randint(0 , num_entries-1)
    entry = entries[index]
    url = reverse("page" , kwargs = {"title" : entry})
    return HttpResponseRedirect(url)
