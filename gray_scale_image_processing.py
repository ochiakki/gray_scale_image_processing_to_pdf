import cv2
import os

# --- 設定項目 ---
# 1. 処理したい画像が入っているフォルダのパスを指定してください
input_folder = '.'  # 例: 'C:/Users/YourName/Desktop/scanned_images'

# 2. 処理後の画像を保存する親フォルダのパスを指定してください
output_folder = 'output_images_multi'

# 3. ★試したいパラメータのリストを指定してください★
#    以下のリストに、試したい値をカンマ区切りで複数入力できます。

# blockSize: 閾値計算に使う領域のサイズ。必ず「奇数」を指定してください。
block_sizes = [11, 21, 31]

# C: 計算された閾値から引かれる定数。
c_values = [3, 5, 7]
# --- 設定はここまで ---


def process_images_with_multiple_params(input_dir, base_output_dir, b_sizes, c_vals):
    """
    指定されたフォルダ内の画像を、複数のパラメータの組み合わせで2値化処理し、
    パラメータごとにサブフォルダを作成して保存する関数。
    """
    # サポートする画像拡張子
    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    # 入力フォルダ内の画像ファイル名を取得
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_extensions)]

    if not image_files:
        print(f"入力フォルダ '{input_dir}' に処理対象の画像が見つかりません。")
        return

    total_combinations = len(b_sizes) * len(c_vals)
    print(f"合計 {total_combinations} 通りのパラメータの組み合わせで処理を開始します。")
    print("-" * 30)

    # パラメータの組み合わせでループ
    for b_size in b_sizes:
        if b_size % 2 == 0:
            print(f"警告: blockSize={b_size} は偶数です。奇数ではないためスキップします。")
            continue

        for c_val in c_vals:
            # パラメータごとにサブフォルダを作成
            sub_output_dir = os.path.join(base_output_dir, f"bs_{b_size}_c_{c_val}")
            if not os.path.exists(sub_output_dir):
                os.makedirs(sub_output_dir)

            print(f"パラメータ (blockSize={b_size}, C={c_val}) で処理中...")

            # 各画像を処理
            for filename in image_files:
                input_path = os.path.join(input_dir, filename)

                try:
                    # 画像をグレースケールで読み込み
                    gray_image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
                    if gray_image is None:
                        print(f"  - 警告: '{filename}' を読み込めませんでした。")
                        continue

                    # 適応的閾値処理を適用
                    binary_image = cv2.adaptiveThreshold(
                        gray_image,
                        255,
                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY,
                        b_size,
                        c_val
                    )

                    # 保存するファイルのパスを作成
                    output_path = os.path.join(sub_output_dir, filename)
                    cv2.imwrite(output_path, binary_image)

                except Exception as e:
                    print(f"  - エラー: '{filename}' の処理中に問題が発生 - {e}")
            
            print(f" -> 結果は '{sub_output_dir}' に保存されました。")

    print("-" * 30)
    print("\nすべての処理が完了しました。")


# メイン処理の実行
if __name__ == '__main__':
    if not os.path.isdir(input_folder):
        print(f"エラー: 入力フォルダ '{input_folder}' が見つかりません。")
        os.makedirs(input_folder, exist_ok=True)
        print(f"サンプルとして '{input_folder}' フォルダを作成しました。処理したい画像を格納してください。")
    else:
        process_images_with_multiple_params(input_folder, output_folder, block_sizes, c_values)