from googletrans import Translator

import logging

logger = logging.getLogger(__name__)

class TranslateSkill:

    def on_load(self, config):
        self._translator = Translator()
        self._default_lang = config.get('configuration').get('target_lang')


    def run(self, context, tools):
        text = context.selection or context.clipboard or ""
        if not text.strip():
            tools.popup.show("Nothing to translate — select or copy text first.")
            return

        target = self._default_lang
        try:
            result = self._translator.translate(text, dest=target.strip())
            tools.popup.show(result.text)
        except Exception as exc:
            tools.popup.show(f"Translation failed: {exc}")
            logger.info(exc)

    def on_error(self, exc):
        pass    # run()