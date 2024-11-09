from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import random
import string
from flask import session


class Controler:
    def receive_notification(self, notification):
        print(f'Notification received: {notification}')
        return notification