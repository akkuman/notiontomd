# notiontomd

Convert notion page content to markdown

## Usage

### Quickstart

`pip install notiontomd`

```python
from notiontomd import NotionToMarkdown

token = os.environ['token']
page_id = os.environ['page_id']

print(NotionToMarkdown(token, page_id).parse())
```

### Feature

Support block:

- paragraph
- numbered_list_item
- bulleted_list_item
- image
- code
- heading_1
- heading_2
- heading_3
- bookmark
- quote
- to_do
- unsupported (The current notion API does not support SimpleTable)
- child_database
- divider
- callout
- video (thanks for [@phuang07](https://github.com/phuang07))
  