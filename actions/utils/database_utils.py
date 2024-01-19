import logging
import os
from typing import Dict, List
import requests
from ..constants import *

logger = logging.getLogger(__name__)

db_server_link = "http://localhost:35000/"

def get_values(
        table,
        column_names: List = [],
        where_condition: Dict = None,
        group_by: List = None,
        order: dict = None,
):
    """Get max row num of table"""
    try:
        response = requests.post(
            f'{db_server_link}retrive/',
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
        logger.error(f'Error: {error}')
        return False


def get_values_by_id(
        table_name,
        column_names: List,
        sender_id: str
):
    """Get max row num of table"""
    try:
        query = f"SELECT {', '.join(column_names)} FROM {table_name} "
        query += f" WHERE id = (SELECT max(id) FROM {table_name} WHERE sender_id = {sender_id} GROUT BY sender_id"
        response = requests.post(
            f"{db_server_link}custom/",
            json = {
                "query": query
            }
        )
        return response.json()
    except (Exception, requests.RequestException) as error:
        logger.error(f'Error: {error}')
        return False


def insert_row(
        table_name,
        **kwargs
):
    """Inserts a row with respective column names in the table with db generated is."""
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


def update_row(
        table_name,
        conditions: Dict,
        update_fields: Dict
):
    """Updates a row inside the table with user id to respective given column names"""
    logger.debug(
        f"table_name: {table_name}\n"
        f"update-conditions: {conditions}\n"
        f"update-field: {update_fields}"
    )
    try:
        response = requests.post(
            f"{db_server_link}update/",
            json={
                "table": table_name,
                "updates": update_fields,
                "where": conditions
            }
        )
        json_response = response.json()
        logger.debug(f"response: {json_response}")
        return True if json_response.get("response") else False
    except (Exception, requests.RequestException) as error:
        logger.error(f"Error: {error}")
        return False


def update_data_using_id(
        table_name,
        sender_id,
        update_fields
):
    """Updates table row using id"""
    logger.debug(
        f"table_name: {table_name}"
        f"sender-id: {sender_id}"
        f"update-field: {update_fields}"
    )
    try:
        response = requests.post(
            f"{db_server_link}update_with_id/",
            json={
                "table": table_name,
                "sender_id": sender_id,
                "updates": update_fields
            }
        )
        json_response = response.json()
        logger.debug(f"response: {json_response}")
        return True if json_response.get("response") else False
    except (Exception, requests.RequestException) as error:
        logger.error(f"Error: {error}")
        return False


def exists_in_col(
        table_name,
        column_name,
        value
):
    """Checks if the given "value" exists in given column of given table.
    Returns: Boolean True if exists else False"""
    try:
        query = (
            f"SELECT EXISTS ( "
            f"SELECT 1 "
            f"FROM {table_name} "
            f"WHERE {column_name} = '{value}') "
            f"AS value_exists;"
        )
        response = requests.post(
            f"{db_server_link}custom/",
            json={
                "query": query
            }
        )
        json_response = response.json()
        if json_response[0][0] is True:
            logger.debug(f'{value} exists in column {column_name} of table {table_name}.')
            return True
        else:
            logger.debug(f'{value} does not exist in column {column_name} of table {table_name}.')
            return False
    except (Exception, requests.RequestException) as error:
        logger.error(f'Error: {error}')
        return False


def delete_row(
        table_name,
        where_condition: dict = None,
        returning: list = None
):
    """Deletes a row from given table with given conditions. If condition is None, deletes all rows.
    Returns columns "returning" if not mentioned mentioned all columns of the delted row."""
    query = f"DELETE FROM {table_name} \n"
    if where_condition:
        where_pairs = [f"{key} = '{value}'" if value else f"{key} is NULL " for key, value in where_condition.items()]
        query += f"WHERE {'AND '.join(where_pairs)} \n"
    query += f"RETURNING {', '.join(returning) if returning  else '*'};\n"
    response = requests.post(
        url=f"{db_server_link}custom/",
        json={
            "query": query
        }
    )
    logger.debug(query)
    json_response = response.json()
    logger.debug(json_response)
    return True
