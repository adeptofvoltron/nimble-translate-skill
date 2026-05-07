![Nimble](logo_mini.png)
# Translator Skill

A skill for the [Nimble](https://github.com/adeptofvoltron/nimble) app that translates selected or clipboard text to any language using Google Translate.

## Usage

Trigger the skill with text selected or copied to clipboard. The translated result appears in a popup.

## Configuration

| Field | Description | Default | Options |
|-------|-------------|---------|---------|
| `target_lang` | Target language code | `en` | `en`, `es`, `fr`, `pl`, `se`, `sr`, `it` |

## Requirements

- Python dependency: `googletrans==4.0.0rc1`
- Nimble permissions: `clipboard`, `popup`

## Installation

Copy this directory into your Nimble skills folder. The `manifest.yaml` is picked up automatically.
