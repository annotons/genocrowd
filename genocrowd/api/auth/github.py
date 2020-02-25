from functools import wraps
from flask import current_app as ca
from flask import Blueprint, request, jsonify, session
from datetime import datetime
from flask_pymongo import BSONObjectIdConverter
from werkzeug.routing import BaseConverter
from genocrowd.libgenocrowd.LocalAuth import LocalAuth

from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

