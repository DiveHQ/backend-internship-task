from flask_testing import TestCase
from flask_crud import create_app, db
from flask_crud.models.user import User
from flask_crud.models.role import Role
from flask_crud.utils.helpers import hash_password

from flask_crud.routes.user_routes import user_blueprint
from flask_crud.routes.entry_routes import entry_blueprint
from flask_crud.routes.setting_routes import setting_blueprint

class TestBase(TestCase):
    def create_app(self):
        app = create_app("testing")
        app.register_blueprint(user_blueprint, url_prefix='/api')
        app.register_blueprint(entry_blueprint, url_prefix='/api')
        app.register_blueprint(setting_blueprint, url_prefix='/api')
        return app

    def setUp(self):
        with self.app.app_context():
            print('Creating tables...')
            db.drop_all()
            db.create_all()
            print('Created tables...')
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.commit()
            admin = User(username='admin', password_hash=hash_password('admin123'), role=admin_role)
            db.session.add(admin)
            db.session.commit()


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            


class TestUser(TestBase):
    def test_create_user(self):
        role = Role.query.filter_by(name='admin').first()
        user = User(username='testuser', password_hash=hash_password('test123'), role=role)
        db.session.add(user)
        db.session.commit()
        added_user = User.query.filter_by(username='testuser').first()
        self.assertEqual(added_user.username, 'testuser')
        print("test_create_user passed")
 

    def test_register(self):
        with self.app.test_request_context():
            response = self.client.post(
                '/api/register/admin',
                json=dict(username='testuser', password='test123'),
                content_type='application/json'
            )
            # print(response.get_json())
            data = response.get_json()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['message'], 'New Admin created! Welcome.')
            print("test_register passed")
