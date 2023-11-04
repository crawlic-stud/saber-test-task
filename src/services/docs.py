import jinja2


TEMPLATE = """
## Description:

{{ description }}

{% if notes %}
## Important moments:

{% for note in notes %}
- {{ note }}
{% endfor %}

{% endif %}

{% if usage %}
## Usage:

{{ usage }}

{% endif %}
"""


JINJA_ENV = jinja2.Environment()


def create(
    description: str,
    notes: list[str] | None = None,
    usage: str | None = None,
) -> str:
    template = JINJA_ENV.from_string(TEMPLATE)
    doc = template.render(description=description, notes=notes, usage=usage)
    return doc
