import importlib.util
import pathlib
from unittest.mock import MagicMock

import pytest


def _load_skill():
    path = pathlib.Path("skill.py")
    spec = importlib.util.spec_from_file_location("translate_skill", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.TranslateSkill


class TestTranslateSkill:

    def setup_method(self):
        self.skill = _load_skill()()
        self.skill.on_load({"target_lang": "fr"})

    def _ctx(self, selection="", clipboard=""):
        ctx = MagicMock()
        ctx.selection = selection
        ctx.clipboard = clipboard
        return ctx

    def test_translates_selection_to_chosen_language(self, mocker):
        mock_result = MagicMock()
        mock_result.text = "Bonjour le monde"
        mock_result.dest = "fr"
        mocker.patch.object(
            self.skill._translator, "translate", return_value=mock_result
        )
        tools = MagicMock()
        tools.input.ask.return_value = "fr"

        self.skill.run(self._ctx(selection="Hello world"), tools)

        tools.clipboard.set.assert_called_once_with("Bonjour le monde")
        tools.popup.show.assert_called_once_with(
            "Translated to fr — copied to clipboard."
        )

    def test_falls_back_to_clipboard_when_no_selection(self, mocker):
        mock_result = MagicMock(text="Hallo Welt", dest="de")
        mocker.patch.object(
            self.skill._translator, "translate", return_value=mock_result
        )
        tools = MagicMock()
        tools.input.ask.return_value = "de"

        self.skill.run(self._ctx(clipboard="Hello world"), tools)

        tools.clipboard.set.assert_called_once_with("Hallo Welt")

    def test_uses_default_lang_when_input_empty(self, mocker):
        mock_result = MagicMock(text="Monde", dest="fr")
        mocker.patch.object(
            self.skill._translator, "translate", return_value=mock_result
        )
        tools = MagicMock()
        tools.input.ask.return_value = ""   # user pressed Enter with no input

        self.skill.run(self._ctx(selection="World"), tools)

        self.skill._translator.translate.assert_called_with("World", dest="fr")

    def test_returns_early_when_nothing_to_translate(self):
        tools = MagicMock()
        self.skill.run(self._ctx(selection="", clipboard=""), tools)
        tools.popup.show.assert_called_once_with(
            "Nothing to translate — select or copy text first."
        )

    def test_returns_early_when_dialog_dismissed(self, mocker):
        mocker.patch.object(self.skill._translator, "translate")
        tools = MagicMock()
        tools.input.ask.return_value = None  # user dismissed

        self.skill.run(self._ctx(selection="Hello"), tools)

        self.skill._translator.translate.assert_not_called()

    def test_shows_popup_on_translation_error(self, mocker):
        mocker.patch.object(
            self.skill._translator, "translate", side_effect=RuntimeError("API down")
        )
        tools = MagicMock()
        tools.input.ask.return_value = "fr"

        self.skill.run(self._ctx(selection="Hello"), tools)

        tools.popup.show.assert_called_once()
        assert "Translation failed" in tools.popup.show.call_args[0][0]