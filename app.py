# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, MedicineStocks, Animal, FoodStocks
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)


@app.route('/')
def index():
    medicines = MedicineStocks.query.all()
    animals = Animal.query.all()
    foods = FoodStocks.query.all()

    food_info = []
    for food in foods:
        animal_name = Animal.query.get(food.animal_id).animal
        food_info.append({'food': food, 'animal_name': animal_name})

    return render_template('index.html', medicines=medicines, animals=animals, foods=food_info)


# CRUD Medicines
@app.route('/medicines', methods=['GET', 'POST'])
def medicines():
    if request.method == 'POST':
        name = request.form['name']
        stock = request.form['stock']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        new_medicine = MedicineStocks(name=name, stock=stock, due_date=due_date)
        db.session.add(new_medicine)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        medicines = MedicineStocks.query.all()
        return render_template('index.html')


@app.route('/delete_medicine/<int:id>')
def delete_medicine(id):
    medicine_to_delete = MedicineStocks.query.get(id)
    db.session.delete(medicine_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


# CRUD Animals
@app.route('/animals', methods=['GET', 'POST'])
def animals():
    if request.method == 'POST':
        animal = request.form['animal']
        breed = request.form['breed']
        new_animal = Animal(animal=animal, breed=breed)
        db.session.add(new_animal)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        animals = Animal.query.all()
        return render_template('index.html', animals=animals)


@app.route('/delete_animal/<int:id>')
def delete_animal(id):
    animal_to_delete = Animal.query.get(id)
    db.session.delete(animal_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


# CRUD Food
@app.route('/foods', methods=['GET', 'POST'])
def foods():
    if request.method == 'POST':
        brand = request.form['brand']
        stock = request.form['stock']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        animal_id = request.form['animal_id'] 
        new_food = FoodStocks(brand=brand, stock=stock, due_date=due_date, animal_id=animal_id)
        db.session.add(new_food)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        foods = FoodStocks.query.all()
        animals = Animal.query.all()
        return render_template('index.html', foods=foods, animals=animals)

@app.route('/delete_food/<int:id>')
def delete_food(id):
    food_to_delete = FoodStocks.query.get(id)
    db.session.delete(food_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
