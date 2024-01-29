from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from models import db, MedicineStocks, Animal, FoodStocks
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
#db.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

swagger = Swagger(app, template={
    "info": {
        "title": "LunalaApp Stocks Management",
        "description": "API for stock management in an animal foundation",
        "termsOfService": "Your Terms of Service",
        "version": "0.0.1",
        "contact": {
            "name": "Maryori Sabalza Mejia",
            "url": "https://github.com/Msabalza730",
            "email": "maryorism730@gmail.com",
        },
    },
})

@app.route('/')
def index():
    """
    Principal View [POST] endpoint.
    ---
    responses:
        200:
            description: Principal page to stocks management, this endpoint is for 'POST' adding new stock:Medicine, Food, new Animals
    """
    medicines = MedicineStocks.query.all()
    animals = Animal.query.all()
    foods = FoodStocks.query.all()

    food_info = []
    for food in foods:
        animal_name = Animal.query.get(food.animal_id).animal
        food_info.append({'food': food, 'animal_name': animal_name})

    return render_template('index.html', medicines=medicines, animals=animals, foods=food_info)


#-----------------------------  CRUD Medicines ---------------------------------------------------
@app.route('/medicines', methods=['GET', 'POST'])
def medicines():
    """
    MEDICINES [GET - POST]  Endpoint.
    ---
    responses:
        200:
            description: Medicine Endpoint to Get Medicines
    """
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


@app.route('/update_medicine/<int:id>', methods=['GET', 'POST'])
def update_medicine(id):
    """
    MEDICINES [UPDATE] endpoint.
    ---
    tags:
        - "UPDATE Methods"
    parameters:
    -   name: id
        in: path
        type: integer
        required: true
        description: ID of the medicine to be updated
    -   name: name
        in: formData
        type: string
        required: true
        description: Edit name for the medicine
    -   name: stock
        in: formData
        type: string
        required: true
        description: Edit stock for the medicine
    -   name: due_date
        in: formData
        type: string
        format: date
        required: true
        description: Edit due date for the medicine
    responses:
        200:
            description: Medicine Endpoint to Update Medicines
    """
    medicine = MedicineStocks.query.get(id)

    if request.method == 'POST':
        medicine.name = request.form['name']
        medicine.stock = request.form['stock']
        medicine.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')

        db.session.commit()

        return redirect(url_for('all_medicines'))

    return render_template('update_medicine.html', medicine=medicine)


@app.route('/delete_medicine/<int:id>', endpoint='delete_medicine')
def delete_medicine(id):
    """
    MEDICINES [DELETE] endpoint.
    ---
    tags:
        - "DELETE Methods"
    parameters:
    -   name: id
        in: path
        type: integer
        required: true
        description: ID of the medicine to be deleted
    responses:
        200:
            description: Medicine Endpoint to DELETE Medicines by ID
    """
    medicine_to_delete = MedicineStocks.query.get(id)
    db.session.delete(medicine_to_delete)
    db.session.commit()
    return redirect(url_for('all_medicines'))


@app.route('/all_medicines')
def all_medicines():
    medicines = MedicineStocks.query.all()
    return render_template('all_medicines.html', medicines=medicines)


# ---------------------------- CRUD Animals ---------------------------------------------------
@app.route('/animals', methods=['GET', 'POST'])
def animals():
    """
    ANIMALS [GET - POST]  Endpoint.
    ---
    responses:
        200:
            description: Medicine Endpoint to Get ANIMALS
    """
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


@app.route('/update_animal/<int:id>', methods=['GET', 'POST'])
def update_animal(id):
    """
    MEDICINES [UPDATE] endpoint.
    ---
    tags:
        - "UPDATE Methods"
    parameters:
    -   name: id
        in: path
        type: integer
        required: true
        description: ID of the animal to be updated
    -   name: Animal
        in: formData
        type: string
        required: true
        description: Edit the Animal 
    -   name: breed
        in: formData
        type: string
        required: true
        description: Breed of the animal
    responses:
        200:
            description: Animal Endpoint to Update Animal
    """
    animal = Animal.query.get(id)
    if request.method == 'POST':
        animal.animal = request.form['animal']
        animal.breed = request.form['breed']

        db.session.commit()

        return redirect(url_for('all_animals'))

    return render_template('update_animal.html', animal=animal)


@app.route('/delete_animal/<int:id>')
def delete_animal(id):
    """
    ANIMALS [DELETE] endpoint.
    ---
    tags:
        - "DELETE Methods"
    parameters:
    -   name: id
        in: path
        type: integer
        required: true
        description: ID of the animal to be deleted
    responses:
        200:
            description: Animal Endpoint to DELETE Animals by ID
    """
    animal_to_delete = Animal.query.get(id)
    db.session.delete(animal_to_delete)
    db.session.commit()
    return redirect(url_for('all_animals'))


@app.route('/all_animals')
def all_animals():
    animals = Animal.query.all()
    return render_template('all_animals.html', animals=animals)


# ------------------------------ CRUD Food ---------------------------------------------------
@app.route('/foods', methods=['GET', 'POST'])
def foods():
    """
    FOOD [GET - POST]  Endpoint.
    ---
    responses:
        200:
            description: FOOD Endpoint to Get FOOD STOCKS
    """
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
    

@app.route('/update_food/<int:id>', methods=['GET', 'POST'])
def update_food(id):
    """
    FOOD [UPDATE] endpoint.
    ---
    tags:
        - "UPDATE Methods"
    parameters:
    -   name: id
        in: path
        type: integer
        required: true
        description: ID of the food to be updated
    -   name: brand
        in: formData
        type: string
        required: true
        description: Edit brand for the animal food
    -   name: stock
        in: formData
        type: string
        required: true
        description: Edit stock for the food
    -   name: due_date
        in: formData
        type: string
        format: date
        required: true
        description: Edit due date for the food
    responses:
        200:
            description: Food Endpoint to Update Food stock
    """
    food = FoodStocks.query.get(id)

    if request.method == 'POST':
        food.brand = request.form['brand']
        food.stock = request.form['stock']
        food.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        food.animal_id = request.form['animal_id']

        db.session.commit()

        return redirect(url_for('all_food'))

    animals = Animal.query.all()
    return render_template('update_food.html', food=food, animals=animals)


@app.route('/delete_food/<int:id>')
def delete_food(id):
    """
    FOOD [DELETE] endpoint.
    ---
    tags:
        - "DELETE Methods"
    parameters:
    -   name: id
        in: path
        type: integer
        required: true
        description: ID of the food to be deleted
    responses:
        200:
            description: Food Endpoint to DELETE Food by ID
    """
    food_to_delete = FoodStocks.query.get(id)
    db.session.delete(food_to_delete)
    db.session.commit()
    return redirect(url_for('all_food'))


@app.route('/all_food')
def all_food():
    foods = FoodStocks.query.all()
    return render_template('all_food.html', foods=foods)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
