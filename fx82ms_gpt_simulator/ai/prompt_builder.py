import json
import os

class PromptBuilder:
    """Builds full AI prompts based on selected mode and raw user input."""
    def __init__(self, templates_path):
        self.templates = {}
        self.load_templates(templates_path)

    def load_templates(self, path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                self.templates = data.get("templates", {})
        except Exception as e:
            print(f"Error loading prompt templates: {e}")

    def build(self, mode: str, user_text: str) -> str:
        """
        Merges user input with a template.
        Example: build("DEFINE", "voltage") -> "Define voltage in a compact way..."
        """
        template = self.templates.get(mode.upper(), "{input}")
        return template.format(input=user_text)
