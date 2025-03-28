#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 03:48:45 2025

@author: Dhananjoy Bhuyan
"""
import os
import json


def _add2json(file_name: str,
              key: str,
              value):
    if os.path.exists(file_name):
        with open(file_name) as f:
            db = json.load(f)
    else:
        db = {}

    db[key] = value

    with open(file_name, "w") as f:
        json.dump(db, f, indent=4)


def store(data,
          key: str,
          database_name: str = "database"):
    if '.' in database_name:
        database_name = database_name.split('.')[0]
    database_name += '.json'

    _add2json(database_name, key, data)


def get(key: str,
        database_name: str = 'database'):
    if '.' in database_name and not database_name.endswith(".json"):
        database_name = database_name.split('.')[0]
    elif '.' not in database_name:
        database_name += '.json'
    if os.path.exists(database_name):
        with open(database_name) as f:
            full_data = json.load(f)
        if not full_data:
            raise KeyError("Database is empty.")
        if key in full_data:
            return full_data[key]
        else:
            raise KeyError(f"Key {key} not found in database.")
    else:
        raise FileNotFoundError("Database not found.")


def remove(key: str,
           database_name: str = 'database'):
    if '.' in database_name and not database_name.endswith(".json"):
        database_name = database_name.split('.')[0]
    elif '.' not in database_name:
        database_name += '.json'
    if os.path.exists(database_name):
        with open(database_name) as f:
            full_data = json.load(f)
        if not full_data:
            raise KeyError("Database is empty.")
        if key in full_data:
            full_data.pop(key)
            return 'success'
        else:
            raise KeyError(f"Key {key} not found in database.")
    else:
        raise KeyError("Database not found.")
