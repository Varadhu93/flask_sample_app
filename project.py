# -*- coding: utf-8 -*-
"""
Created on Thu May 16 23:35:28 2019

@author: S.R.Varadharam-pc
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# CODE TO RETURN RESTAURANTS BASED ON RESTAURANT ID
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)
#    output = ''
#    for i in items:
#        output += i.name
#       output += '</br>'
#       output += i.price
#        output += '</br>'
#        output += i.description
#        output += '</br>'
#        output += '</br>'
#    return output


# CODE TO DELETE A MENU ITEM
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Item has been deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deleteItem)


# CODE TO EDIT A MENU ITEM IN A RESTAURANT
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        # if request.form['course']:
        #     editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# CODE TO CREATE A NEW RESTAURANT MENU ITEM
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# CODE TO EDIT RESTAURANT
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):

    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        # restaurant = Restaurant(name=request.form['name'])
        if request.form['name']:
            restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)


# CODE TO SHOW RESTAURANTS
@app.route('/restaurants', methods=['GET', 'POST'])
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    if request.method == 'GET':
        return render_template('restaurants.html', restaurants=restaurants)

if __name__ == '__main__':
    app.secret_key = 'super_secretkey'
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
