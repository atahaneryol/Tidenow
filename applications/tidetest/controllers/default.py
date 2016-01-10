# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from gluon import current
import logging

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
    import datetime
    fulldate = datetime.datetime.today()
    if fulldate.minute > 30:
        minute_part = 30
    else:
        minute_part = 0

    restaurantList = db((db.currentDiscounts.day_time==fulldate.weekday()+1) &
                        (db.currentDiscounts.hour_time==fulldate.hour) &
                        (db.currentDiscounts.min_time==minute_part) ).select(db.currentDiscounts.ALL, orderby=~db.currentDiscounts.discount)
    #TODO take min of 3 restaurants. Where empty discounts count as 100. But if there are 3 empty discounts then the discount is 0.
    #TODO make the closed restaurants grey and sold outs red in HTML-CSS.

    #min(restaurantList.discount,restaurantList2.discount,restaurantList3.discount)
    return dict(allRest=restaurantList)

def restaurant():
    clickedRestaurant = request.args[0]

    # The argument will have dashes instead of spaces. Replace them
    clickedRestaurant = clickedRestaurant.replace("-"," ")
    restaurantInfo = db(db.restaurants.name==clickedRestaurant).select(db.restaurants.ALL, orderby=~db.restaurants.discount, limitby=(0,1)).first()
    paymentStatus = "Not Done"
    if restaurantInfo:
        #Stripe handling:
        from gluon.contrib.stripe import Stripe
        key="sk_test_GCahWSkWRdvnTUzF8cHDUUKQ"
        testPostVars = request.post_vars
        logging.info("In pay3 stuff: " + str(testPostVars))
        if testPostVars['stripeToken']:
            token = request.post_vars['stripeToken']
            amountTotal = int(request.post_vars['inputAmount'])*100
            d = Stripe(key).charge(
                       amount=amountTotal,
                       currency='usd',
                       token=token,
                       description='test charge')
            logging.info(str(d))
            paymentStatus = d['status'].title()
        return dict(singleRest=restaurantInfo,status=paymentStatus)
    else:
        return "No restaurant with name: " + clickedRestaurant

def pay3():
    from gluon.contrib.stripe import Stripe
    key="sk_test_GCahWSkWRdvnTUzF8cHDUUKQ"
    testPostVars = request.post_vars
    logging.info("In pay3 stuff: " + str(testPostVars))
    if testPostVars:
        token = request.post_vars['stripeToken']
        amountTotal = int(request.post_vars['amount'])*100
        d = Stripe(key).charge(
                   amount=amountTotal,
                   currency='usd',
                   token=token,
                   description='test charge')
        logging.info(str(d))
        return dict(form=d)
    return dict(form=testPostVars)

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
    #db.restaurants.insert(name="Joya", description="Latin American, Tapas Bar", logoURL="extra/static/logos/joya.png", discount=36)
    return "Success"

def fillDBFromCSV():
    import csv
    import os
    filepath = os.path.join(request.folder,'static/files','site_database_dec12.csv')
    csvFile = open(filepath,"rb")
    reader = csv.reader(csvFile)
    rownum = 0
    resString = ""
    for row in reader:
        # Save header row.
        if rownum == 0:
            header = row
        else:
            name = row[0]
            region = row[1]
            res_id = row[2]
            day = row[3]
            hour = row[4]
            minute = row[5]
            if row[6]!="":
                discount = float(row[6])*100
            else:
                discount = -999
            openTime = row[7]
            cuisine = row[8]
            isopen = row[9]
            member = row[10]
            db.restaurants.insert(name=name, region=region, restaurant_id=res_id, day_time=day, hour_time=hour, min_time=minute, open_hours_display=openTime,
                                  cuisine=cuisine, isopen_correct=isopen, member_restaurant=member, discount=discount)
        rownum += 1
    csvFile.close()
    return "Success"

def runRestaurantDiscountCalculation():
    db(db.currentDiscounts.id>0).delete()
    import datetime
    fulldate = datetime.datetime.today()
    if fulldate.minute > 30:
        minute_part = 30
    else:
        minute_part = 0

    restaurantList = db((db.restaurants.day_time==fulldate.weekday()+1) &
                        (db.restaurants.hour_time==fulldate.hour) &
                        (db.restaurants.min_time==minute_part) ).select(db.restaurants.ALL, orderby=~db.restaurants.discount)
    for singleRest in restaurantList:
        # Get the other two discount values for a particular restaurant.
        disc1 = singleRest.discount
        disc2 = db( (db.restaurants.name==singleRest.name) &
                    (db.restaurants.day_time==fulldate.weekday()+1) &
                    (db.restaurants.hour_time==fulldate.hour+1) &
                    (db.restaurants.min_time==minute_part) ).select(db.restaurants.ALL, limitby=(0,1)).first().discount

        disc3 = db( (db.restaurants.name==singleRest.name) &
                    (db.restaurants.day_time==fulldate.weekday()+1) &
                    (db.restaurants.hour_time==fulldate.hour+2) &
                    (db.restaurants.min_time==minute_part)).select(db.restaurants.ALL, limitby=(0,1)).first().discount

        minVal=min(abs(disc1),abs(disc2),abs(disc3))
        if minVal==999:
            # Means it is closed
            singleRest.discount=-1
        else:
            singleRest.discount=minVal
        db.currentDiscounts.insert(name=singleRest.name, region=singleRest.region, restaurant_id=singleRest.restaurant_id, day_time=singleRest.day_time, hour_time=singleRest.hour_time,
                                   min_time=singleRest.min_time, open_hours_display=singleRest.open_hours_display, cuisine=singleRest.cuisine, isopen_correct=singleRest.isopen_correct,
                                   member_restaurant=singleRest.member_restaurant, discount=singleRest.discount)
    logging.info("Discount Calculation successful.")
    return "Discount calculation successful."

def clearDB():
    db(db.restaurants.id>0).delete()
    db(db.currentDiscounts.id>0).delete()
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


