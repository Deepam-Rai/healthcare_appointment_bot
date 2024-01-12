import os
import logging
from typing import Dict, List
import requests
from utils.constants import *
logger = logging.getLogger(__name__)
db_server_link = LOCAL_DB_SERVER


def get_values(
    table,
    column_names: List = [],
    where_condition: Dict = None,
    group_by: List = None,
    order: dict = None,
):
    """
    Get max row num of table
    """
    try:
        response = requests.post(
            f"{db_server_link}retrive/",
            json={
                "table": table,
                "columns": column_names,
                "where": where_condition,
                "groupby": group_by,
                "order": order,
            },
        )
        return response.json()

    except (Exception, requests.RequestException) as error:
        logger.error("Error: %s" % error)
        return False


def get_values_by_id(table_name, column_names: List, sender_id: str):
    """
    Get max row num of table
    """
    try:
        query = ""
        query = f"SELECT {', '.join(column_names)} from {table_name} "
        query += f"WHERE id = (Select max(id) from {table_name} where sender_id = '{sender_id}' group by sender_id)"
        response = requests.post(f"{db_server_link}custom/", json={"query": query})
        all_data = response.json()
        return all_data

    except (Exception, requests.RequestException) as error:
        logger.error("Error: %s" % error)
        return False


def insert_row(table_name, **kwargs):
    """
    insert row inside table name with user id with respective column names in kwargs
    """
    logger.debug(f"table_name: {table_name}\n" f"insert-kwargs: {kwargs}")
    try:
        response = requests.post(
            f"{db_server_link}insert/", json={"table": table_name, "data": kwargs}
        )
        json_response = response.json()
        logger.debug(f"response: {json_response}")
        return (
            (True, json_response.get("id"))
            if json_response.get("response")
            else (False, -1)
        )

    except (Exception, requests.RequestException) as error:
        logger.error("Error: %s" % error)
        return (False, -1)


def update_row(table_name, conditions: Dict, update_fields: Dict):
    """
    update row inside table name with user id with respective column names in kwargs
    """
    logger.debug(
        f"table_name: {table_name}\n"
        f"udpate-conditions: {conditions}\n"
        f"update-field: {update_fields}"
    )
    try:
        response = requests.post(
            f"{db_server_link}update/",
            json={"table": table_name, "updates": update_fields, "where": conditions},
        )
        json_response = response.json()
        logger.debug(f"response: {json_response}")
        return True if json_response.get("response") else False

    except (Exception, requests.RequestException) as error:
        logger.error("Error: %s" % error)
        return False


def update_data_using_id(table_name, sender_id, update_fields):
    """
    Update table row using id -> Nested query
    """
    logger.debug(
        f"table_name: {table_name}\n"
        f"sender-id: {sender_id}\n"
        f"update-field: {update_fields}"
    )
    try:
        response = requests.post(
            f"{db_server_link}update_with_id/",
            json={
                "table": table_name,
                "sender_id": sender_id,
                "updates": update_fields,
            },
        )
        json_response = response.json()
        logger.debug(f"response: {json_response}")
        return True if json_response.get("response") else False

    except (Exception, requests.RequestException) as error:
        logger.error("Error: %s" % error)
        return False
