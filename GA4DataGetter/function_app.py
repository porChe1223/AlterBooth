import azure.functions as func
import logging
import json
import datetime
import concurrent.futures
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric, OrderBy
import time
import os


#############################
## GA4からのレポート情報取得 
## - GA4の設定
##   GA4で1つのディメンショングループと全てのメトリクスからレポート取得
##   並列処理
##
# ディメンションとメトリクスの読み込み
def make_list(textfile):
    with open(textfile, 'r') as f:
        lists = f.readlines()
    return [list.strip() for list in lists if list.strip()]
# GA4のプロパティID
ga4_property_id = os.getenv('GA4_PROPERTY_ID')

# GA4の設定
KEY_FILE_LOCATION = 'ga4Alterbooth.json'           # サービスアカウントJSONファイルのパス
DIMENSIONS = make_list('GA4DimensionsMain.txt') # ディメンション
METRICS= make_list('GA4MetricsMain.txt')        # メトリクス
ORDER_BY_METRIC = None                          # 並び替えのメトリクス
LIMIT = 1000                                    # 結果の制限数
PROPERTY_ID = ga4_property_id                   # GA4のプロパティID

# GA4で1つのディメンショングループと全てのメトリクスからレポート取得
def get_report_parallel(
    start_date: str,
    end_date: str,
    dimension: list,
    metrics: list,
    order_by: str = None,
    limit: int = 1000,
):
    #======================================
    # 並列処理
    # - メトリクスをまとめて取得
    #
    #======================================
    try:
        # クライアントの初期化
        client = BetaAnalyticsDataClient.from_service_account_file(KEY_FILE_LOCATION)
        # レスポンスリストの初期化
        responses = []

        # 文字列をリストに変換
        dimension_list = eval(dimension)
        # ディメンショングループからまとめて作成
        dim = [Dimension(name=dims) for dims in dimension_list]
        # メトリクスを10個ずつまとめて作成
        for i in range(0, len(metrics), 7):
            divided_metrics = metrics[i : i + 7]
            met = [Metric(name=mets) for mets in divided_metrics]

            # 一括リクエスト
            request = RunReportRequest(
                property=f'properties/{PROPERTY_ID}',
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                dimensions=dim,
                metrics=met,
                limit=limit,
            )
            # レポートの実行
            response = client.run_report(request)

            # レスポンスをレスポンスリストに追加
            responses.append(response)
            logging.info(f'[SUCCESS]: Dimension: {dimension}, Metric: {met}')

        return responses 

    except Exception as e:
        logging.error(f'[FAIL]: Dimension: {dimension}, Metric: {met}')
        logging.error(e)

    # レスポンスリストを返す
    return responses


    #================================
    # 並列処理ができない場合
    # - ネストでループ処理
    # - タイムアウトになるため却下
    #
    #================================
    # try:
    #     # クライアントの初期化
    #     client = BetaAnalyticsDataClient.from_service_account_file(KEY_FILE_LOCATION)
    #     # レスポンスリストの初期化
    #     responses = []
        
    #     # １つのディメンショングループと全てのメトリクスからレポート取得
    #     for metric in metrics:
    #         try:
    #             # 文字列をリストに変換
    #             dimension_list = eval(dimension)
    #             # ディメンションとメトリクスを設定
    #             dim = [Dimension(name=dims) for dims in dimension_list]
    #             met = [Metric(name=metric)]

    #             # レポートリクエストの作成
    #             request = RunReportRequest(
    #                 property=f'properties/{PROPERTY_ID}',
    #                 date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    #                 dimensions=dim,
    #                 metrics=met,
    #                 order_bys=None,
    #                 limit=limit,
    #             )

    #             # レポートの実行
    #             response = client.run_report(request)
    #             # レスポンスをレスポンスリストに追加
    #             responses.append(response)
    #             logging.info(f'[SUCCESS]: Dimension: {dimension}, Metric: {metric}')
    #         except Exception as e:
    #             logging.error(f'[FAIL]: Dimension: {dimension}, Metric: {metric}')
    #             logging.error(e)
        
    #     # レスポンスリストを返す
    #     return responses
    
    # except Exception as e:
    #     logging.error(f'ERROR: GA4レポート取得中にエラーが発生しました')
    #     logging.error(e)
    #     raise


###############################
## レポート情報をJSON型に変換
##
def format_response_as_json(responses):
    try:
        result = []
        def process_response(response):
            for row in response.rows:
                data = {
                    "dimensions": {dim.name: dim_value.value for dim, dim_value in zip(response.dimension_headers, row.dimension_values)},
                    "metrics": {metric.name: metric_value.value for metric, metric_value in zip(response.metric_headers, row.metric_values)}
                }
                result.append(data)
        
        # リストである場合
        if isinstance(responses, list):
            for response in responses:
                process_response(response)
        # 単一のRunReportResponseオブジェクトである場合
        else:
            process_response(responses)
        
        return json.dumps(result, indent=4, ensure_ascii=False)

    except Exception as e:
        logging.error(f'JSON形式への変換中にエラーが発生しました: {e}')
        raise

#################################
## Main関数
## - HTTPリクエストを受け取り
##   GA4からレポート情報を取得
##   レポート情報をCOSMOSDBに格納
##   HTTPレスポンスで出力
##
app = func.FunctionApp()
@app.function_name(name='GA4DataGetter')
@app.route(route='data', auth_level=func.AuthLevel.ANONYMOUS)
@app.queue_output(arg_name='msg', queue_name='outqueue', connection='AzureWebJobsStorage')
@app.cosmos_db_output(
    arg_name = 'outputDocument',
    database_name = 'my-database',
    container_name = 'Alterbooth_AA DOJO',
    connection = 'COSMOS_DB_CONNECTION_STRING'
)

def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage], outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    try:
        # パラメータの定義
        range = req.params.get('range')
        # パラメータからレポートの範囲指定
        if not range:
            today = datetime.date.today()                      # 今日の日付
            last_month = today - datetime.timedelta(days=30)   # 1か月前
            START_DATE = str(last_month)                       # レポートの開始日(今日)
            END_DATE = str(today)                              # レポートの終了日(1か月前)
            DATE_RANGE = START_DATE+'to'+END_DATE              # レポートの範囲(アイテムのIDに相当)
        else:
            START_DATE = range.split('to')[0]                  # レポートの開始日(指定日)
            END_DATE = range.split('to')[1]                    # レポートの終了日(指定日)
            DATE_RANGE = range                                 # レポートの範囲(アイテムのIDに相当)

        # CosmosDBデータリスト初期化
        docs = []
        # HTTPレスポンスリスト初期化
        http_response = []

        # カテゴリーの定義
        categories = [
            'ページ関連情報',
            'トラフィックソース関連情報',
            'ユーザー行動関連情報',
            'サイト内検索関連情報',
            'デバイスおよびユーザ属性関連情報',
            '時間帯関連情報'
        ]

        # ディメンショングループとカテゴリーを対応させてレポート取得
        for dimension, category in zip(DIMENSIONS, categories):
            # GA4レポート取得
            logging.info(f'[START]: {category} のレポート情報取得')
            response = get_report_parallel(
                START_DATE,
                END_DATE,
                dimension,
                METRICS,
                ORDER_BY_METRIC,
                LIMIT
            )
            logging.info(f'[END]: {category} のレポート情報取得')

            # レポート情報をJSON型に変換
            logging.info('開始: Json化')
            response_json = format_response_as_json(response)
            logging.info('終了: Json化')

            # レポート情報を格納する辞書の初期化
            doc = {
                'id': f'{DATE_RANGE}-{category}',
                '日付の範囲': DATE_RANGE,
                category: json.loads(response_json) 
            }

            # Cosmos DB 用にドキュメントに変換して格納
            docs.append(func.Document.from_dict(doc))

            # HTTP レスポンスにも追加（ここでは一旦 doc をそのまま突っ込む）
            http_response.append(doc)

        # CosmosDB用に格納
        logging.info('[START]: CosmosDBに出力')
        outputDocument.set(docs)
        # 処理完了メッセージをFunctionsのキューに追加
        msg.set('Report processed')
        logging.info('[END]: CosmosDBに出力')

        # HTTPレスポンスリストに追加
        http_response.append(doc)
        # HTTPレスポンスを返す
        return func.HttpResponse(
            body = json.dumps(
                http_response,
                ensure_ascii=False,
                indent=4
            ),
            status_code=200,
            mimetype='application/json'
        )
    except Exception as e:
        logging.error(f'エラーが発生しました: {e}')
        return func.HttpResponse(f'エラーが発生しました: {e}', status_code=500)
