# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
第一回(app.ask)では、文脈によってことなる場合があることを述べ、一般論として回答を生成。
具体的な可能性が高い2つのパターンを解説していた。
だが今回(app.agent)では、AIE講座におけるレベル3の定義をもとに回答を行っている。
関係する回は示されていなかった。
- `--trace` で見えたツール呼び出し（ツール名と引数）：
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
- 1つの質問での LLM 呼び出し回数（`requests`）：2回
- 追加したツールと、docstring に書いた説明：
def make_quiz(lecture: int) -> str:
    """指定した回の用語から 1つを選び、
    確認問題と答えを返す。
    「第2回の確認問題を出して」のように、
    復習用の問題を求められたときに使う。
    """
    terms = [term for term in load_glossary() if term["lecture"] == lecture]
    if not terms:
        return f"第{lecture}回の用語は用語集にありません。"

    term = random.choice(terms)
    return json.dumps(
        {
            "question": f"「{term['definition']}」に当てはまる用語は何ですか？",
            "answer": term["term"],
        },
        ensure_ascii=False,
    )
## 宿題

- 取り組んだレベル：基礎
- やったこと：
INSTRUCTIONSから"- 回答の最後に、関係する回（第N回）を示す。"を削除し、
解答の違いについて確認した。
- 結果：実際に削除前は"関連する回：第2回"と最後に出力していた。
削除後は目的通り、削除前で見られたこの出力は見られなかった。
削除前のtrace:
--- trace ---
[tool call]   make_quiz({'lecture': 2})
[tool return] make_quiz -> {"question": "「LoRAで使う低ランク行列の大きさを決めるハイパーパラメータ。大きいほど表現力が上がるが、学習するパラメータとメモリも増える。」に当てはまる用語は何ですか？", "answer": "ランク（LoRAのr）"}…
[usage] RunUsage(cost=Decimal('0.0005049'), details={'text_prompt_tokens': 883}, input_text_tokens=883,input_tokens=883, output_tokens=96, requests=2, tool_calls=1)

削除後のtrace:
--- trace ---
[tool call]   make_quiz({'lecture': 2})
[tool return] make_quiz -> {"question": "「モデルの重みを少ないビット数（例：16ビットから4ビット）で表し、メモリ使用量や計算量を減らす技術。精度は少し下がることがある。」に当てはまる用語は何ですか？", "answer": "量子化"}…
[usage] RunUsage(cost=Decimal('0.0005100'), details={'text_prompt_tokens': 850}, input_text_tokens=850,input_tokens=850, output_tokens=102, requests=2, tool_calls=1)

- 気づき・疑問：今回はINSTRUCTIONSの変更のみだったのでtraceには二回の試行で問題が変わっていることくらいしか変わっていなかった。このINSTRUCTIONSやdocstringの内容を変えるだけで、モデルの挙動を変えれることがよく分かった。
