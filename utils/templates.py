# utils/templates.py

def load_template(template_type: str = "default") -> str:
    templates = {
        "default": (
            "Hello, I came across your project titled '{job_title}' and would love to help. "
            "I specialize in {expertise} and can deliver a high-quality result tailored to your needs."
        ),
        "legal": (
            "Dear Client, I reviewed your legal tech project titled '{job_title}'. "
            "With my experience in building legal bots and automation tools, I'm confident I can assist you."
        )
    }
    return templates.get(template_type, templates["default"])
