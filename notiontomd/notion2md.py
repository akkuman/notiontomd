import json
from notion_client import Client

class NotSupportType(TypeError):
    pass

class ElementAnnotations:
    def __init__(self, data: dict):
        self.bold = data.get('bold', False)
        self.italic = data.get('italic', False)
        self.strikethrough = data.get('strikethrough', False)
        self.underline = data.get('underline', False)
        self.code = data.get('code', False)
        self.color = data.get('color', 'default')
    
    def parse_text(self, text):
        parsed_text = text
        if self.bold:
            parsed_text = f'**{parsed_text}**'
        if self.italic:
            parsed_text = f'*{parsed_text}*'
        if self.strikethrough:
            parsed_text = f'~~{parsed_text}~~'
        if self.underline:
            parsed_text = f'<u>{parsed_text}</u>'
        if self.code:
            parsed_text = f'`{parsed_text}`'
        if self.color != 'default':
            parsed_text = f'<font color={self.color}>{parsed_text}</font>'
        return parsed_text


class NotionToMarkdown:
    def __init__(self, token, page_id):
        self.notion = Client(auth=token)
        self.page_id = page_id
    
    def get_blocks(self, parent_block_id):
        page_data = self.notion.blocks.children.list(parent_block_id)
        return page_data.get('results') or []

    def _parse_blocks(self, blocks, level=0):
        text = ''
        for block in blocks:
            block_type = block.get('type')
            text += '  ' * level + getattr(self, f'handle_block_{block_type}')(block, level) + '\n\n'
            if block.get('has_children'):
                text += self._parse_blocks(self.get_blocks(block['id']), level+1)
        return text
    
    def parse(self) -> str:
        blocks = self.get_blocks(self.page_id)
        return self._parse_blocks(blocks)
    
    def _handle_element_base(self, element):
        '''处理块内元素的基础方法'''
        plain_text = element.get('plain_text', '')
        href = element.get('href', '')
        annotations = ElementAnnotations(element.get('annotations', {}))
        parsed_text = plain_text
        if href:
            parsed_text = f'[{parsed_text}]({href})'
        parsed_text = annotations.parse_text(parsed_text)
        return parsed_text

    def handle_element_text(self, element):
        '''处理块内text元素'''
        return self._handle_element_base(element)
    
    def handle_element_mention(self, element):
        '''处理块内mention元素，目前仅支持link_preview'''
        mention_field = element.get('mention', {})
        if mention_field.get('type') != 'link_preview':
            raise NotSupportType('不支持mention元素link_preview之外的类型')
        return self._handle_element_base(element)
    
    def _handle_text_block_base(self, block, level=0):
        '''处理text块的基础方法'''
        block_type = block.get('type')
        texts = block.get(block_type, {}).get('text', [])
        block_text = ''
        for element in texts:
            element_type = element.get('type')
            block_text += getattr(self, f'handle_element_{element_type}')(element)
        return block_text

    def handle_block_paragraph(self, block: dict, level=0):
        '''处理paragraph类型的块'''
        return self._handle_text_block_base(block)

    def handle_block_numbered_list_item(self, block, level=0):
        '''处理numbered_list_item类型的块'''
        block_text = self._handle_text_block_base(block)
        return f'1. {block_text}'
    
    def handle_block_bulleted_list_item(self, block, level=0):
        '''处理bulleted_list_item类型的块'''
        block_text = self._handle_text_block_base(block)
        return f'- {block_text}'

    def handle_block_image(self, block, level=0):
        image_field = block.get('image', {})
        image_file_url = image_field.get('file', {}).get('url', '')
        return f'![]({image_file_url})'
    
    def handle_block_code(self, block, level=0):
        '''处理code类型的块'''
        block_text = self._handle_text_block_base(block)
        lang = block.get('code', {}).get('language', '')
        if level > 0:
            code_text = ''
            for line in block_text.split('\n'):
                code_text +=  4 * ' ' + line + '\n' + '  ' * level
                print(json.dumps(code_text), level)
            return code_text
        else:
            return f'```{lang}\n{block_text}\n```'
    
    def handle_block_heading_1(self, block, level=0):
        '''处理heading_1类型的块'''
        block_text = self._handle_text_block_base(block)
        return f'# {block_text}'
    
    def handle_block_heading_2(self, block, level=0):
        '''处理heading_2类型的块'''
        block_text = self._handle_text_block_base(block)
        return f'## {block_text}'
    
    def handle_block_heading_3(self, block, level=0):
        '''处理heading_3类型的块'''
        block_text = self._handle_text_block_base(block)
        return f'### {block_text}'
    
    def handle_block_bookmark(self, block, level=0):
        '''处理bookmark类型的块'''
        bookmark_field = block.get('bookmark', {})
        bookmark_url = bookmark_field.get('url', '')
        return f'- [{bookmark_url}]({bookmark_url})'
    
    def handle_block_quote(self, block, level=0):
        '''处理quote类型的块'''
        block_text = self._handle_text_block_base(block)
        return f'> {block_text}'
