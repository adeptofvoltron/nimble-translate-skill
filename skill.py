from googletrans import Translator


class TranslateSkill:

    def on_load(self, config):
        self._translator = Translator()
        self._default_lang = config.get("target_lang", "en")

    def run(self, context, tools):
        text = context.selection or context.clipboard
        if not text.strip():
            tools.popup.show("Nothing to translate — select or copy text first.")
            return

        target = tools.input.ask(
            f"Translate to (e.g. fr, de, ja) [{self._default_lang}]:"
        )
        if target is None:          # user dismissed the dialog
            return
        if not target.strip():
            target = self._default_lang

        try:
            result = self._translator.translate(text, dest=target.strip())
            tools.clipboard.set(result.text)
            tools.popup.show(f"Translated to {result.dest} — copied to clipboard.")
        except Exception as exc:
            tools.popup.show(f"Translation failed: {exc}")

    def on_error(self, exc):
        pass    # run() a