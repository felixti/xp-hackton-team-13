import logging
import os
import azure.functions as func
from azure.data.tables import TableServiceClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    change_number = req_body.get("change_number")
    configuration_item =  req_body.get("configuration_item")
    planned_start_date = req_body.get("planned_start_date")
    planned_end_date = req_body.get("planned_start_date")
    
    logging.info(f'Processando solicitação de registro de janela de manutenção no Zabbix para mudança: {change_number}')

    # TODO: Call Zabbix and register new maintenance alert window for requested configuration item

    register_maintenance_alert_window_request(change_number, configuration_item, planned_start_date, planned_end_date)

    return func.HttpResponse(
            f'Recebi as seguintes informacoes: {change_number} - {configuration_item} - {planned_start_date} - {planned_end_date}',
            status_code=200
    )

def register_maintenance_alert_window_request(change_number, configuration_item, planned_start_date, planned_end_date):
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