import logging
from pprint import pformat
import traceback

import intersight.api.telemetry_api
import intersight.model.telemetry_druid_data_source
import intersight.model.telemetry_druid_period_granularity
import intersight.model.telemetry_druid_query_context
import intersight.model.telemetry_druid_time_series_request
import credentials

FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def get_time_series(api_client):
    """Query Druid time series"""

    # Create an instance of the API telemetry service.
    api_instance = intersight.api.telemetry_api.TelemetryApi(api_client)
    logger.info("Query 'ucs_ether_port_stat' time series")
    req = intersight.model.telemetry_druid_time_series_request.TelemetryDruidTimeSeriesRequest(
        query_type="timeseries",
        data_source=intersight.model.telemetry_druid_data_source.TelemetryDruidDataSource(
            type="table",
            name="ucs_ether_port_stat",
        ),
        intervals=[
            "2021-01-01T00:00:00.000Z/2021-01-15T00:00:00.000Z",
        ],
        granularity=intersight.model.telemetry_druid_period_granularity.TelemetryDruidPeriodGranularity(
            type="period",
            period="P1D",
        ),
        context=intersight.model.telemetry_druid_query_context.TelemetryDruidQueryContext(
            timeout=30,
            query_id="ucs_ether_port_stat-QueryIdentifier",
        ),
    )
    api_response = api_instance.query_telemetry_time_series(
        telemetry_druid_time_series_request=req,
    )
    logger.info(pformat(api_response))

    ##########################
    logger.info("Query 'device_connector' time series")
    req = intersight.model.telemetry_druid_time_series_request.TelemetryDruidTimeSeriesRequest(
        query_type="timeseries",
        data_source=intersight.model.telemetry_druid_data_source.TelemetryDruidDataSource(
            type="table",
            name="device_connector",
        ),
        intervals=[
            "2021-01-01T00:00:00.000Z/2021-01-15T00:00:00.000Z",
        ],
        granularity=intersight.model.telemetry_druid_period_granularity.TelemetryDruidPeriodGranularity(
            type="period",
            period="P1D",
        ),
        context=intersight.model.telemetry_druid_query_context.TelemetryDruidQueryContext(
            timeout=30,
            query_id="device_connector-QueryIdentifier",
        ),
    )
    api_response = api_instance.query_telemetry_time_series(
        telemetry_druid_time_series_request=req,
    )
    logger.info(pformat(api_response))

    ##########################
    logger.info("Query 'PSU stat' time series")
    req = intersight.model.telemetry_druid_time_series_request.TelemetryDruidTimeSeriesRequest(
        aggregations=[
            intersight.model.telemetry_druid_aggregator.TelemetryDruidAggregator(
                field_name="sumEnergyConsumed",
                type="doubleSum",
                name="energyConsumed",
                field_names=["sumEnergyConsumed"]
            ),
        ],
        query_type="timeseries",
        data_source=intersight.model.telemetry_druid_data_source.TelemetryDruidDataSource(
            type="table",
            name="psu_stat",
        ),
        intervals=[
            "2021-01-01T00:00:00.000Z/2021-01-15T00:00:00.000Z",
        ],
        granularity=intersight.model.telemetry_druid_period_granularity.TelemetryDruidPeriodGranularity(
            type="period",
            period="P1D",
        ),
        context=intersight.model.telemetry_druid_query_context.TelemetryDruidQueryContext(
            timeout=30,
            query_id="psu_stat-QueryIdentifier",
        ),
    )
    api_response = api_instance.query_telemetry_time_series(
        telemetry_druid_time_series_request=req,
    )
    logger.info(pformat(api_response))


def main():
    # Configure API key settings for authentication
    api_client = credentials.config_credentials()

    try:
        # Get example time series data
        get_time_series(api_client)

    except intersight.OpenApiException as e:
        logger.error("Exception when calling API: %s\n" % e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
