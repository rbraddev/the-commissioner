from jinja2 import Environment, FileSystemLoader, StrictUndefined
from app.settings import Settings, get_settings

settings: Settings = get_settings()

def render_file(template, **kwargs):

    env = Environment(
        loader=FileSystemLoader(settings.TEMPLATE_DIR),
        undefined=StrictUndefined,
        trim_blocks=True
    )

    template = env.get_template(template)
    return template.render(**kwargs)