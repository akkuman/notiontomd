# notiontomd

Convert notion page content to markdown

## Usage

### Quickstart

`pip install notiontomd`

```python
from notiontomd import NotionToMarkdown

token = os.environ['token']
database_id = os.environ['database_id']

print(NotionToMarkdown(token, page_id).parse())
```