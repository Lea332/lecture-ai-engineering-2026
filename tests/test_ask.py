from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=7),
        text="回答",
    )
    captured = {}

    class FakeModels:
        def generate_content(self, **kwargs):
            captured.update(kwargs)
            return response

    class FakeClient:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)

    assert ask_module.ask("質問", temperature=0.0) == "回答"
    assert captured["config"].temperature == 0.0
    assert capsys.readouterr().out == "[tokens] 入力: 12, 出力: 7\n"