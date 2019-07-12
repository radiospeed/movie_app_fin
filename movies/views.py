from django.shortcuts import render, redirect
from django.contrib import messages
#for notifications
from airtable import Airtable
import os

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
             'Movies',
             api_key=os.environ.get('AIRTABLE_API_KEY'),)
        #environ and environment are different!

def home_page(request):
    #this shows all movies, its not just a sesrch function. If we redirect to root page, this function runs to show all movies
    #print("hello: " + str(request.GET.get('query','')))
    user_query = str(request.GET.get('query', ''))
    ##goes into the GET methdd. whstever query is, get that
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    #user_query.lower() this lowers the string on backend
    #LOWER({Name} this lowercases the name on the airtable end
    stuff_for_frontend = {'search_result': search_result}
    #context dictrionary
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)



def create(request):
    print(request.POST.get('name'))
    if request.method == 'POST':
        data = {
            #'airtable field name': request.post.get (this refers to the data from the request form sent from create-moda;.html)('name of the field in out FORM in create-modal')
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/No_image_available_600_x_450.svg/600px-No_image_available_600_x_450.svg.png'}],

            #https://www.filmonpaper.com/site/media/2013/11/DeathProof_onesheet_international-1-500x738.jpg
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            print("pic is:")
            print (data['Pictures'])
            response = AT.insert(data)
            #before, we only has thi like like: AT.insert(data)
            #but when we run inert command,
            #airtable sends back a dictionary, which tells us which movie got added
            #so we're going to put that dictionary it sends back into a variable

            messages.success(request, 'New movie added: {}'.format(response['fields'].get('Name')))
            #we could have used response['fields']['Name'], it would return the same thing
            #but 'get' function will not throw an error snd crash program if the 'Name'
            #key does not exist. it will just ignore it and move on. This is the
            #benefit of using get instead of writing response['fields']['Name']
            #
            #Also, we didn't write response['fields'][0]['Name'] because the returned
            #dictrionsry that insert function give us does not have multiple elementd like
            #[0], [1] etc. You csn see this by running the response = insert ine
            #in terminal, then see the dictionary inside response
        except Exception as e:
            messages.warning(request, 'Got an error when trying to create a new movie: {}'.format(e))

    return redirect('/')
    #take me back to yourapp.com root. it runs the home_page function

def edit(request, movie_id):
    print('url is here:')
    print(request.POST.get('url'))


    if "https://dl.airtable.com/.attachments" in request.POST.get('url') or "https://upload.wikimedia.org/" in request.POST.get('url'):
        new_url = request.POST.get('url')[:-1]
        print('new url is:')
        print(new_url)

    else:
        new_url = request.POST.get('url')
        print('new url is:')
        print(new_url)

    #see airtableurl_notes for explanation of why we needed to do this

    if request.method == 'POST':
            data = {

                'Name': request.POST.get('name'),
                    #<label for="editName">Name</label>
                    #<input type="text" class="form-control" id="editName" placeholder="Enter name" name="name" value="{{ movie.fields.Name }}" />
                    #we are NOT pulling 'editName'. That is a name id for the form. We pull from the name='name'

                #pictures is a list of dictionaries, so you can't go:
                    #'Pictures': request.POST.get('url')
                    #else you get an error Unprocessable Entity for url: https://api.airtable.com/v0/appK2cLqnsYQL9icU/Movies/rec9ypbL2u5y76S0T
                    #how do you know it's a list of dictionaries? you can use the terminal to look up
                    #a record like 'Interstallar' and you'll see in the Pictures field,
                    #it starts as a list [] and then inside is a dictionary {}
                'Pictures': [{'url': new_url or 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/No_image_available_600_x_450.svg/600px-No_image_available_600_x_450.svg.png'}],
                'Rating': int(request.POST.get('rating')),
                    #note: you will get sn error if you don't manually enter a new rating.
                    #atm original rating does not populate here
                'Notes': request.POST.get('notes')
            }
            try:
                response = AT.update(movie_id, data)
                #notify on update
                messages.success(request, 'Movie updated: {}'.format(response['fields'].get('Name')))
            except Exception as e:
                messages.warning(requedt, 'Got an error while trying to update a movie: {}'.format(e))



    return redirect('/')


def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        #get name from movie id
        response = AT.delete(movie_id)
        messages.warning(request, 'Movie has been deleted: {}'.format(movie_name))
    except Exception as e:
        messages.warning(request, 'Got an error while trying to delete: {}'.format(e))
    return redirect('/')

# Create your views here.
