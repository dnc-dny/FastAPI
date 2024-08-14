import uvicorn #uvicorn: ASGIサーバーで、FastAPIアプリケーションを実行するために使用
from fastapi import FastAPI #FastAPI: FastAPIのメインクラス
from fastapi.openapi.utils import get_openapi #get_openapi: FastAPIがデフォルトで生成するOpenAPIスキーマをカスタマイズするための関数
from pydantic import BaseModel #BaseModel: Pydanticのベースモデルクラスで、データ検証のために使用

app = FastAPI() #FastAPIアプリケーションのインスタンスを作成

def custom_openapi(): #custom_openapi 関数
    if app.openapi_schema: #app.openapi_schema が既に存在する場合はそれを返し
        return app.openapi_schema
    openapi_schema = get_openapi( #存在しない場合は get_openapi を使って新しいスキーマを生成
        title="Example Web API", #APIのタイトル
        version="0.0.1", #APIのバージョン
        description="FastAPIで作ったWebAPIです。", #APIの説明
        routes=app.routes, #APIのルート情報
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi #このカスタム関数を app.openapi に設定することで、FastAPIはカスタムOpenAPIスキーマを使用


class Item(BaseModel): #Item クラスはPydanticの BaseModel を継承しており、リクエストボディとして使用されるデータモデルを定義
    name: str #nameは文字列string
    price: int #priceは整数integer


#エンドポイントには summary と description を追加し、APIドキュメントの説明を充実させる
@app.get(
    "/items/{item_name}", #/items/{item_name} のパスに対してGETリクエストが来た時に呼ばれる関数を定義
    summary="アイテム取得",
    description="指定されたアイテムを取得し返却します。",
)
def get_item(item_name: str): #get_item関数を定義
    return {"name": item_name, "price": 200} #リクエストで指定されたitem_nameを含む辞書を返し、priceは固定で200


@app.post(
    "/items/new", #/items/new のパスに対してPOSTリクエストが来た時に呼ばれる関数を定義
    summary="アイテム追加",
    description="渡されたアイテムを追加します。",
)
def add_item(item: Item): #item引数：リクエストのデータがItemクラスに従っていることを期待
    return item #add_item関数：リクエストのデータ（Itemオブジェクト）をそのまま返す


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080) #uvicorn.run 関数を使用してapp(FastAPIアプリケーション)を0.0.0.0というホストと8080というポートで起動
