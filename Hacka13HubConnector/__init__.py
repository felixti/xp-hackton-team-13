import logging
import os
import datetime as dt
from pytz import timezone
import azure.functions as func
from azure.data.tables import TableServiceClient

try:
    from pyzabbix.api import ZabbixAPI
except ImportError:
    logging.error("missing py-zabbix dependency")


def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    change_number = req_body.get("change_number")
    short_description = req_body.get("short_description")
    configuration_item =  req_body.get("configuration_item")
    planned_start_date = req_body.get("planned_start_date")
    planned_end_date = req_body.get("planned_end_date")
    
    logging.info(f'Processando solicitação de registro de janela de manutenção no Zabbix para mudança: {change_number}')

    start_date = dt.datetime.strptime(planned_start_date, '%Y-%m-%d %H:%M:%S')
    end_date = dt.datetime.strptime(planned_end_date, '%Y-%m-%d %H:%M:%S')
    register_maintenance_period(change_number, host_id=configuration_item, description=short_description, start_date=start_date, end_date=end_date)
    register_maintenance_period_log(change_number, configuration_item, planned_start_date, planned_end_date)

    return func.HttpResponse(
            f'Janela de Manutenção cadastrada para mudança: {change_number}',
            status_code=201
    )

def register_maintenance_period_log(change_number, configuration_item, planned_start_date, planned_end_date):
    connection_string = os.environ["AzureWebJobsStorage"]
    table_name = os.environ["EntityName"]

    service = TableServiceClient.from_connection_string(conn_str=connection_string)
    
    table_client = service.create_table_if_not_exists(table_name)

    entity = {
        'PartitionKey': configuration_item,
        'RowKey': change_number,
        'PlannedStartDate': planned_start_date,
        'PlannedEndDate': planned_end_date,
    }

    table_client.create_entity(entity)

def get_host_id(zapi, host_name=None):
    result = zapi.do_request('host.get', {"search": {"name": host_name}})['result']
    if result and len(result) > 0:
        return result[0]['hostid']

def create_maintenance(zapi, host_id=None, name=None, description=None, start=None, end=None):
    param = {
        "groupids": [],
        "hostids": [host_id],
        "name": name,
        "maintenance_type": "0",
        "description": description,
        "active_since": str(start),
        "active_till": str(end),
        "timeperiods": [
            {
                "timeperiod_type": 0,
                "start_date": str(start),
                "period": end-start
            }]
    }
    return zapi.do_request('maintenance.create', params=param)

# Press the green button in the gutter to run the script.
def register_maintenance_period(change_number, host_id, description, start_date, end_date):
    server_url = os.environ["ZabbixServerUrl"]
    login_user = os.environ["ZabbixLogin"]
    login_password = os.environ["ZabbixPassword"]
    # Create ZabbixAPI class instance
    with ZabbixAPI(url=server_url, user=login_user, password=login_password) as zapi:
        host_id = get_host_id(zapi, host_id)
        sao_paulo_timezone = timezone('America/Sao_Paulo')
        start = int(start_date.replace(tzinfo=sao_paulo_timezone).timestamp())
        end = int(end_date.replace(tzinfo=sao_paulo_timezone).timestamp())
        maintenance = create_maintenance(zapi, host_id=host_id, name=change_number, description=description, start=start, end=end)
        logging.info(maintenance)