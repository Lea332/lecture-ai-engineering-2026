# 第5回 解答

## 演習

- 回答モデル（実行時の`[model]`）：
- 比較した質問：
- 対象資料（全文投入と他の方式で範囲が違う点も記録）：

### 各方式の結果

| 方式 | 回答の要点・正しさ | 引用ページと根拠 | 時間（秒） | 入力／出力トークン数 | モデル応答回数 | 生成API推定費用（USD） |
|---|---|---|---|---|---|---|
| 全文投入 |正答|第2回 p.51, 52|4.22 秒|入力 117,025 tokens / 出力 253 tokens|モデル応答 1 回|$0.004784 USD|
| ベクトル検索 |正答|第2回 p.51, 52|4.39 秒|入力 3,027 tokens / 出力 198 tokens|モデル応答 2 回|$0.001403 USD|
| Tree |正答|第2回 p.51, 52|11.16 秒|入力 4,199 tokens / 出力 260 tokens |モデル応答 4 回|$0.001910 USD|
| Graph |正答|第2回 p.51, 52|8.47 秒|入力 5,773 tokens / 出力 230 tokens|モデル応答 2 回|$0.002307 USD|

<!-- 未実行・算定不可の場合は、その旨を書いてください。質問を追加した場合は、質問ごとに表を分けてください。 -->

- 検索だけを実行して見つかったページと、その本文で確認できたこと：
検索結果 1はページ52を検索。質問の答えの核となる部分を検索出来た。その他51ページや60ページなど関連性の高いものが引っ張ってこれた。
- `--trace`で見えたツール呼び出し（ツール名・引数・回数、Treeでたどった目次など）：
一個目
[tool call]   search_materials({'query': 'LoRA QLoRA 固定 学習'})
[tool return] search_materials -> {"results": [{"page_id": "lec02-main-p052", "document_id": "lec02-main", "lecture": 2, "document_title": "基盤モデルの仕組み", "s…
二個目
[tool call]   glossary_search_glossary({'query': 'LoRA'})
[tool call]   glossary_search_glossary({'query': 'QLoRA'})
[tool return] glossary_search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] glossary_search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[tool call]   glossary_search_glossary({'query': 'PEFT'})
[tool call]   glossary_search_glossary({'query': '量子化'})
[tool return] glossary_search_glossary -> [{"term": "PEFT", "lecture": 2, "definition": "モデルの全パラメータではなく、ごく一部や追加した小さなパラメータだけを学習する手法の総称。必要なGPUメモリと保存容量を大きく減らせる。LoRAが…
[tool return] glossary_search_glossary -> [{"term": "量子化", "lecture": 2, "definition": "モデルの重みを少ないビット数（例：16ビットから4ビット）で表し、メモリ使用量や計算量を減らす技術。精度は少し下がることがある。", "relate…
[tool call]   glossary_search_glossary({'query': '第2回'})
[tool return] glossary_search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
三個目
[tool call]   search_graph({'query': 'LoRA 固定 QLoRA 追加'})
[tool return] search_graph -> {"seeds": [{"page_id": "lec02-main-p052", "document_id": "lec02-main", "lecture": 2, "document_title": "基盤モデルの仕組み", "sec…
- 取得した情報が足りなかった例、取得できたのに回答へ使えなかった例：特になし。
- 今回の用途に採用したい方式と、その理由・比較条件の限界：ベクトル検索の方式がモデルの応答回数、API推定費用共に低い記録を出していたため、ベクトル検索を採用したい。
これがもし、複雑になった問題や多くの次元を扱う問題の時、どうなるかが比較できない。
- 気づき・疑問：
RAGの技術を使うことによってAPI費用を削減かつ正答率をあげることができることを知った。
あまり疑問は思い浮かばなかった。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 
- やったこと（変更したファイル・設定・処理、または設計した取得方法）：RAG_TOP_Kを5から3に変更
- 比較した質問と、固定した条件（モデル・対象資料など）：
質問は第2回の説明では、LoRAは何を固定し何を学習しますか？ QLoRAは何を加えますか？
固定した条件はこのRAG_TOP_K以外。
- 結果（変更前後の回答・根拠、`--trace`の出力、時間・トークン数・生成API推定費用など）：
変更前
[tool call]   search_materials({'query': 'LoRA QLoRA 固定 学習'})
[tool return] search_materials -> {"results": [{"page_id": "lec02-main-p052", "document_id": "lec02-main", "lecture": 2, "document_title": "基盤モデルの仕組み", "s…
[time] 回答完了まで 4.39 秒（検索・埋め込みを含む）
[usage] 入力 3,027 tokens / 出力 198 tokens / モデル応答 2 回
[cost] 生成APIの推定コスト: $0.001403 USD（埋め込み・索引構築分は含まない）
変更後
[tool call]   search_materials({'query': 'LoRA QLoRA 固定 学習'})
[tool return] search_materials -> {"results": [{"page_id": "lec02-main-p052", "document_id": "lec02-main", "lecture": 2, "document_title": "基盤モデルの仕組み", "s…
[time] 回答完了まで 9.07 秒（検索・埋め込みを含む）
[usage] 入力 2,077 tokens / 出力 169 tokens / モデル応答 2 回
[cost] 生成APIの推定コスト: $0.001046 USD（埋め込み・索引構築分は含まない）
- 改善した例と、残る失敗・制約：
RAGの検索数が減ったおかげで入力のtokensが3027から2077に減った。また出力のtokensも198から169に減った。
- 気づき・疑問：
一方、実行時間は4.39秒から9.07秒へ増加した。
そのため、検索結果を減らすと必ず処理時間が短くなるとは言えない。
APIの応答時間や検索処理のばらつきが影響した可能性があると考えられる。
実行時間が必ずしも減るとは限らないと知った。
ほかにもいろんなことを試して、要因を多角的にみれるようになりたい。
他にも要因がないか気になった。