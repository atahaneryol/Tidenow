# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from gluon import current

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def index2():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #db = current.db
    restaurantList = db(db.restaurants.id>0).select(db.restaurants.ALL, orderby=~db.restaurants.discount)
    return dict(allRest=restaurantList)

def fillDummyDB():
    # This fills the DB with dummy restaurants
    #db = current.db
    db.restaurants.insert(name="Ephesus", description="Turkish and Greek", logoURL="extra/static/logos/ephesus_logo.png", discount=31)
    db.restaurants.insert(name="Cafe Baklava", description="Mediterranean Grill", logoURL="extra/static/logos/cafe_baklava_logo.png", discount=43)
    db.restaurants.insert(name="Evvia", description="Greek", logoURL="extra/static/logos/evvia.png", discount=12)
    db.restaurants.insert(name="Galata Bistro", description="Mediterranean", logoURL="extra/static/logos/galata_logo.png", discount=26)
    db.restaurants.insert(name="Olympus", description="Bakery, Breakfast & Lunch", logoURL="extra/static/logos/olympus_logo.png", discount=17)
    db.restaurants.insert(name="Shana", description="Thai", logoURL="extra/static/logos/shana.png", discount=49)
    db.restaurants.insert(name="Tamarine", description="Vietnamese", logoURL="extra/static/logos/tamarine.png", discount=14)
    db.restaurants.insert(name="Joya", description="Latin American, Tapas Bar", logoURL="extra/static/logos/joya.png", discount=36)
    return "Success"

def clearDB():
    db(db.restaurants.id>0).delete()
    return "DB cleared."

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


