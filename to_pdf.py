import os
from PIL import Image, ImageOps

# --- 設定項目 ---

# 1. 出力するPDFファイルの名前を指定してください
output_pdf_path = "A4_filled_output.pdf"

# 2. 検索する画像の拡張子（小文字で指定）
SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']


# --- ここから下は通常変更する必要はありません ---

# A4サイズ (横) をピクセルで定義 (300 DPIの場合)
A4_LANDSCAPE_PIXELS = (3507, 2481)
DPI = 300.0

def create_pdf_from_images_in_folder():
    """
    スクリプトが置かれているフォルダ内の全画像を、
    A4横サイズいっぱいに拡大（クロップ）してPDFに変換する
    """
    pdf_pages = []
    
    # スクリプトがあるフォルダのパスを取得
    current_directory = os.getcwd()

    # フォルダ内の画像ファイルを名前順にリストアップ
    image_files = sorted([
        f for f in os.listdir(current_directory)
        if os.path.isfile(f) and f.lower().endswith(tuple(SUPPORTED_EXTENSIONS))
    ])

    if not image_files:
        print("フォルダ内に処理対象の画像ファイルが見つかりませんでした。")
        print(f"対応している拡張子: {', '.join(SUPPORTED_EXTENSIONS)}")
        return

    print("処理を開始します...")
    print(f"見つかった画像ファイル ({len(image_files)}件):")
    for f in image_files:
        print(f" - {f}")
    print("-" * 20)


    for image_file in image_files:
        try:
            with Image.open(image_file) as img:
                print(f"'{image_file}' を処理中...")

                # 画像をRGBモードに変換
                img_rgb = img.convert("RGB")

                # ▼▼▼ 変更点 ▼▼▼
                # 元画像の縦横比を維持したまま、A4横サイズに合うように拡大し、
                # はみ出す部分を中央からトリミング（クロップ）する
                page = ImageOps.fit(
                    img_rgb, 
                    A4_LANDSCAPE_PIXELS, 
                    Image.Resampling.LANCZOS # 高画質なリサイズ方法を指定
                )
                # ▲▲▲ 変更ここまで ▲▲▲

                pdf_pages.append(page)

        except Exception as e:
            print(f"エラー: '{image_file}' の処理中に問題が発生しました: {e}")

    if pdf_pages:
        pdf_pages[0].save(
            output_pdf_path,
            "PDF",
            resolution=DPI,
            save_all=True,
            append_images=pdf_pages[1:]
        )
        print("-" * 20)
        print(f"処理が完了しました。PDFファイル '{output_pdf_path}' が作成されました。")
    else:
        print("\n処理できる画像がなかったため、PDFは作成されませんでした。")

if __name__ == "__main__":
    create_pdf_from_images_in_folder()