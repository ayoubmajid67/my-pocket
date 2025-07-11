from flask import Flask, jsonify,request
from sqlalchemy import text
from flask import Blueprint

from app.db import db
from app.models.test import Test


tests_bp = Blueprint('tests', __name__)

@tests_bp.route('/checkDbConnexion')
def healthcheck():
    try:
        # Execute a simple query to test the connection
        db.session.execute(text('SELECT 1'))
        return jsonify(status='success', message='Database connection is healthy'), 200
    except Exception as e:
        print("\n\n------------error------- \n\n")
        print(e)
        return jsonify(status='error', message=f'Database connection failed: {str(e)}'), 500
    


# 1. Create - Add a New Record (Using ORM)
@tests_bp.route('/addTestDataORM', methods=['POST'])
def add_test_data_orm():
    try:
        data = request.get_json()
        new_test = Test(firstname=data['firstname'], lastname=data['lastname'])
        db.session.add(new_test)
        db.session.commit()
        return jsonify(status='success', message='Test data added successfully'), 201
    except Exception as e:
        print("\n\n------------error------- \n\n", e)
        return jsonify(status='error', message=f'Error adding test data: {str(e)}'), 500

# 2. Create - Add a New Record (Using Direct SQL Query)
@tests_bp.route('/addTestDataSQL', methods=['POST'])
def add_test_data_sql():
    try:
        data = request.get_json()
        query = text('INSERT INTO test (firstname, lastname) VALUES (:firstname, :lastname)')
        db.session.execute(query, {'firstname': data['firstname'], 'lastname': data['lastname']})
        db.session.commit()
        return jsonify(status='success', message='Test data added successfully'), 201
    except Exception as e:
        print("\n\n------------error------- \n\n", e)
        return jsonify(status='error', message=f'Error adding test data: {str(e)}'), 500

# 3. Read - Get All Records (Using ORM)
@tests_bp.route('/getTestDataORM', methods=['GET'])
def get_test_data_orm():
    try:
        tests = Test.query.all()
        test_data = [{'id': test.id, 'firstname': test.firstname, 'lastname': test.lastname} for test in tests]
        return jsonify(status='success', data=test_data), 200
    except Exception as e:
        print("\n\n------------error------- \n\n", e)
        return jsonify(status='error', message=f'Error fetching test data: {str(e)}'), 500

# 4. Read - Get All Records (Using Direct SQL Query)
@tests_bp.route('/getTestDataSQL', methods=['GET'])
def get_test_data_sql():
    try:
        query = text('SELECT * FROM test')
        result = db.session.execute(query)
        test_data = [{'id': row[0], 'firstname': row[1], 'lastname': row[2]} for row in result.fetchall()]
        return jsonify(status='success', data=test_data), 200
    except Exception as e:
        print("\n\n------------error------- \n\n", e)
        return jsonify(status='error', message=f'Error fetching test data: {str(e)}'), 500

# 5. Update - Edit an Existing Record (Using ORM)
@tests_bp.route('/updateTestDataORM/<int:id>', methods=['PUT'])
def update_test_data_orm(id):
    try:
        data = request.get_json()
        test = Test.query.get(id)
        if test:
            test.firstname = data['firstname']
            test.lastname = data['lastname']
            db.session.commit()
            return jsonify(status='success', message='Test data updated successfully'), 200
        else:
            return jsonify(status='error', message='Test data not found'), 404
    except Exception as e:
        print("\n\n------------error------- \n\n", e)
        return jsonify(status='error', message=f'Error updating test data: {str(e)}'), 500

# 6. Update - Edit an Existing Record (Using Direct SQL Query)
@tests_bp.route('/updateTestDataSQL/<int:id>', methods=['PUT'])
def update_test_data_sql(id):
    try:
        data = request.get_json()
        query = text('UPDATE test SET firstname = :firstname, lastname = :lastname WHERE id = :id')
        db.session.execute(query, {'firstname': data['firstname'], 'lastname': data['lastname'], 'id': id})
        db.session.commit()
        return jsonify(status='success', message='Test data updated successfully'), 200
    except Exception as e:
        print("\n\n------------error------- \n\n", e)
        return jsonify(status='error', message=f'Error updating test data: {str(e)}'), 500

# 7. Delete - Delete a Record (Using ORM)
@tests_bp.route('/deleteTestDataORM/<int:id>', methods=['DELETE'])
def delete_test_data_orm(id):
    try:
        test = Test.query.get(id)
        if test:
            db.session.delete(test)
            db.session.commit()
            return jsonify(status='success', message='Test data deleted successfully'), 200
        else:
            return jsonify(status='error', message='Test data not found'), 404
    except Exception as e:
        print("\n\n------------error------- \n\n", e)
        return jsonify(status='error', message=f'Error deleting test data: {str(e)}'), 500

# 8. Delete - Delete a Record (Using Direct SQL Query)
@tests_bp.route('/deleteTestDataSQL/<int:id>', methods=['DELETE'])
def delete_test_data_sql(id):
    try:
        query = text('DELETE FROM test WHERE id = :id')
        db.session.execute(query, {'id': id})
        db.session.commit()
        return jsonify(status='success', message='Test data deleted successfully'), 200
    except Exception as e:
        print("\n\n------------error------- \n\n", e)
        return jsonify(status='error', message=f'Error deleting test data: {str(e)}'), 500