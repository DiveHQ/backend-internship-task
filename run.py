from flask_crud import app, db
from flask_crud.routes.user_routes import user_blueprint
from flask_crud.routes.entry_routes import entry_blueprint
from flask_crud.routes.setting_routes import setting_blueprint

from flask_crud import app, db
from flask_crud.models.role import Role

# import logging
# from logging import StreamHandler



# Register Blueprints
app.register_blueprint(user_blueprint, url_prefix='/api/v1')
app.register_blueprint(entry_blueprint, url_prefix='/api/v1')
app.register_blueprint(setting_blueprint, url_prefix='/api/v1')


# app.logger.setLevel(logging.INFO)
# app.logger.addHandler(StreamHandler())




if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
            if not Role.query.filter_by(name='admin').first():
                admin_role = Role(name='admin')
                db.session.add(admin_role)
            if not Role.query.filter_by(name='user_manager').first():
                user_manager_role = Role(name='user_manager')
                db.session.add(user_manager_role)
            if not Role.query.filter_by(name='regular_user').first():
                regular_user_role = Role(name='regular_user')
                db.session.add(regular_user_role)
            db.session.commit()
            print('Tables created.')
            print('Starting the app...')
        app.run(debug=True, port=4747)
    except Exception as e:
        print(e)
        print('Failed to run the app.')