import os
import re
import uuid

class MarkdownParser:
    def __init__(self):
        self.image_regex = r'!\[([^\]]*)\]\(([^)]+)\)'

    def parse_images(self, content: str):
        """
        Parses the images in the Markdown content.
        :param content:
        :return: List of dictionaries containing image information
        """
        images = []
        for match in re.finditer(self.image_regex, content):
            images.append({
                'id': str(uuid.uuid4()),
                'alt_text': match.group(1),
                'path': match.group(2),
                'start': match.start(),
                'end': match.end(),
                'original': match.group(0)
            })
        return images

    def replace_image_paths(self, content: str, base_path: str):
        """
        Replaces the image paths with absolute paths.
        :param content:
        :param base_path:
        :return:
        """
        def replace(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            if not image_path.startswith(('http://', 'https://')):
                abs_path = os.path.abspath(os.path.join(base_path, image_path))
                return f'![{alt_text}]({abs_path})'
            return match.group(0)

        return re.sub(self.image_regex, replace, content)
