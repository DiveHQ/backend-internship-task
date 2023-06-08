from flask_crud import app, db
from flask_crud.models.entry import Entry
from flask_crud.models.setting import Setting
from flask_crud.models.user import User
from flask_crud.models.role import Role

with app.app_context():
    db.create_all()
    admin_role = Role(name='admin')
    user_manager_role = Role(name='user_manager')
    regular_user_role = Role(name='regular_user')
    db.session.add(admin_role)
    db.session.add(user_manager_role)
    db.session.add(regular_user_role)
    db.session.commit()