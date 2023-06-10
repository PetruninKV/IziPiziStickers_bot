from datetime import datetime
import logging
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client.client.exceptions import InfluxDBError

from config_data.config import config


async def log(tags_dict):
    data = {
        "measurement": "bot_commands",
        "time": datetime.utcnow().isoformat(),
        "fields": {"event": 1},
        "tags": tags_dict,
    }
    try:
        async with InfluxDBClientAsync(
            url=config.influxdb.host,
            token=config.influxdb.token,
            org=config.influxdb.org,
        ) as client:
            ready = await client.ping()
            logging.info(f"InfluxDB: {ready}")
            write_api = client.write_api()
            successfully = await write_api.write(bucket=config.influxdb.db, record=data)
            logging.info(f" > successfully: {successfully}")
    except InfluxDBError as ex:
        logging.error(f"InfluxDB write error: {str(ex)}")
