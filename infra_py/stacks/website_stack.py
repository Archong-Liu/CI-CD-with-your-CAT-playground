"""
🎉 歡迎來到 AWS CDK 工作坊！🎉

這個 stack 會幫你建立一個超棒的「S3 靜態網站」解決方案（無 CloudFront/OAC）：
- 🗄️ S3 靜態網站託管：直接用 S3 提供網站內容
- 🚀 自動部署：前端 build 後自動同步到 S3

今天你會學到：
1. 🔒 如何設定 S3 靜態網站託管
2. 🗂️ 如何讓網站頁面正確回應（index.html / 錯誤頁）
3. 🤖 使用 CDK 自動部署前端資產到 S3

準備好了嗎？讓我們開始吧！✨
"""

from typing import Optional
import aws_cdk as cdk
from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
)
from constructs import Construct


class WebsiteStack(cdk.Stack):
    """
    🌟 靜態網站部署 Stack（S3-only）🌟

    這個 stack 會建立一個好懂、好用的 S3 靜態網站環境：
    - 🗄️ S3 靜態網站託管（直接用 S3 當網站主機）
    - 🤖 自動化部署流程（一鍵同步前端資產）

    超適合入門與教學的工作坊！🎓
    """
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ========================================
        # 🎯 步驟 1: 建立 S3 靜態網站 Bucket
        # ========================================
        # S3 就是你的網站小主機 🏠
        # 這裡我們直接啟用「靜態網站託管」，讓瀏覽器能透過 S3 網站端點讀取內容
        # 小提醒：S3 靜態網站端點僅支援 HTTP，因此不要設定 enforce_ssl
        website_bucket = s3.Bucket(
            self,
            "WebsiteBucket",
            website_index_document="index.html",  # 首頁檔案
            website_error_document="index.html",  # SPA/錯誤回到首頁
            public_read_access=True,               # 對外可讀（CDK 會自動加上公開讀取的 Bucket Policy）
            block_public_access=s3.BlockPublicAccess.BLOCK_ACLS,  # 使用 Policy 控制公開權限
            encryption=s3.BucketEncryption.S3_MANAGED,            # 基本加密，簡單安全
        )

        # ========================================
        # 🚀 步驟 2: 部署前端資產到 S3
        # ========================================
        # 一鍵把 build 好的網站同步到 S3，超方便！
        # 路徑預設為 ../website/dist（請先在 website/ 內執行 npm run build）
        s3deploy.BucketDeployment(
            self,
            "DeployWebsiteAssets",
            destination_bucket=website_bucket,
            sources=[s3deploy.Source.asset("../website/dist")],
        )


