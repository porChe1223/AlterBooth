import azure.functions as func
import logging
import json
import os
from dotenv import load_dotenv
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric, OrderBy


###########################
# GA4からのレポート情報取得 #
###########################
load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # Google Cloudの認証情報設定

if GOOGLE_APPLICATION_CREDENTIALS:
    print(f"Google Cloud Credentials Path: {GOOGLE_APPLICATION_CREDENTIALS}")
else:
    print("環境変数 'GOOGLE_APPLICATION_CREDENTIALS' が設定されていません。")

KEY_FILE_LOCATION = "ga4account.json" # サービスアカウントJSONファイルのパス

PROPERTY_ID = "469101596" # GA4のプロパティID

START_DATE = "2022-12-28" # レポートの開始日
END_DATE = "2024-12-30" # レポートの終了日
DIMENSIONS = ["pagePath", "pageTitle", "city", "country", "browser", "operatingSystem", "deviceCategory"]   # ディメンション
METRICS = ["screenPageViews", "sessions", "totalUsers", "newUsers", "bounceRate", "averageSessionDuration"] # メトリクス
ORDER_BY_METRIC = "screenPageViews" # 並び替えのメトリクス
LIMIT = 100000 # 結果の制限数

def get_ga4_report(start_date, end_date, dimensions, metrics, order_by_metric=None, limit=100000):
    try:
        # クライアントの初期化
        client = BetaAnalyticsDataClient.from_service_account_file(KEY_FILE_LOCATION)

        # ディメンションとメトリクスをオブジェクト化
        dimension_objects = [Dimension(name=dim) for dim in dimensions]
        metric_objects = [Metric(name=metric) for metric in metrics]

        # 並び替えの設定
        order_by = None
        if order_by_metric:
            order_by = [OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_by_metric), desc=True)]
        
        # レポートリクエストの設定
        request = RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=dimension_objects,
            metrics=metric_objects,
            order_bys=order_by,
            limit=limit,
        )
        # レポートの取得
        return client.run_report(request)
    
    except Exception as e:
        logging.error(f'GA4レポート取得中にエラーが発生しました: {e}')
        raise



############################
# レポート情報をJSON型に変換 #
############################

def format_response_as_json(response):
    try:
        result = []
        for row in response.rows:
            data = {
                "dimensions": {dim_name: dim_value.value for dim_name, dim_value in zip([dim.name for dim in response.dimension_headers], row.dimension_values)},
                "metrics": {metric_name: metric_value.value for metric_name, metric_value in zip([metric.name for metric in response.metric_headers], row.metric_values)}
            }
            result.append(data)
        return json.dumps(result, indent=4, ensure_ascii=False)
    
    except Exception as e:
        logging.error(f'JSON形式への変換中にエラーが発生しました: {e}')
        raise



##############################
# レポート情報をCOSMOSDBに格納 #
##############################

app = func.FunctionApp()
@app.function_name(name="InputGA4Info")
@app.route(route="data", auth_level=func.AuthLevel.ANONYMOUS)
@app.queue_output(arg_name="msg", queue_name="outqueue", connection='AzureWebJobsStorage')
@app.cosmos_db_output(arg_name="outputDocument", database_name="my-database", container_name="my-container", connection='COSMOS_DB_CONNECTION_STRING')

def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage], outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    try:                                                                                           # 結果の制限数
        # GA4からのレポート情報取得
        response = get_ga4_report(START_DATE, END_DATE, DIMENSIONS, METRICS, ORDER_BY_METRIC, LIMIT)
        logging.info('GAのレポート取得情報')

        # レポート情報をJSON型に変換
        results = format_response_as_json(response)
        logging.info('レポート情報Json化')

        # Cosmos DB に出力
        outputDocument.set(func.Document.from_dict({"id": "report", "data": results}))
        logging.info('CosmosDBに出力')

        msg.set("Report processed")
        logging.info('Queueにメッセージを送信')

        # JSONレスポンスを返す
        return func.HttpResponse(results, status_code=200)
    
    except Exception as e:
        logging.error(f'エラーが発生しました: {e}')
        return func.HttpResponse(f'エラーが発生しました: {e}', status_code=500)
