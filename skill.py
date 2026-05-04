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

        target = "sr"

        try:
            result = self._translator.translate(text, dest=target.strip())
            tools.clipboard.set(result.text)
            tools.popup.show(f"Translated to {result.dest} — copied to clipboard.")
        except Exception as exc:
            tools.popup.show(f"Translation failed: {exc}")

    def on_error(self, exc):
        pass    # run() a