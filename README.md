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