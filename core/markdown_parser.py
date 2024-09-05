import re
import os

class MarkdownParser:
    def __init__(self):
        self.image_regex = r'!\[([^\]]*)\]\(([^)]+)\)'

    def parse_images(self, content):
        return [(match.group(2), match.start(), match.end()) for match in re.finditer(self.image_regex, content)]

    def replace_image_paths(self, content, base_path):
        def replace(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            if not image_path.startswith(('http://', 'https://')):
                abs_path = os.path.abspath(os.path.join(base_path, image_path))
                return f'![{alt_text}]({abs_path})'
            return match.group(0)

        return re.sub(self.image_regex, replace, content)
