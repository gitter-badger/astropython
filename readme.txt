About the project : Astropython
>> The entire project has been broken down into apps - with each app name denoting the components it handles
>> The data ported from the old website is present in the ported directory
>> The project configuration is available in the astropython directory
>> The template directory holds templates for the entire project
>> populate.py is a population script for populating our databases initially

Regarding the general structure of the apps :-
>> admin.py : Deals with the admin functionality of the specific app
>> managers.py : Adding query functionalities to our models (managing our models)
>> models.py : Models of our app . Each model is automatically transalted to DB schemas
>> moderator.py : Moderation setting for our app
>> tests.py : App specific testing scripts
>> forms.py : Contains form data to be used in the views
>> views.py : Front-end - Back-end interface and evaluation scripts

Quick set of commands to run the project :-
1.Check virtual environment and Install requirements
2.python manage.py makemigrations
3.python manage.py migrate
4.python manage.py collectstatic
5.python populate.py
6.python manage.py runserver

Goto /admin to access admin panel and under the tab "Django Moderations" approve all posts(especially the wiki post- that is the main Wiki Page)... It would take some time. SQLite 3 is pretty slow , let it complete

Join the chat at https://gitter.im/x-calibre/astropython
