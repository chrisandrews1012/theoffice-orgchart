"""
Shared CSS styles and helper functions for Streamlit pages.
Eliminates CSS duplication across pages.
"""


def get_base_styles() -> str:
    """
    Get base CSS styles for all pages.

    :return: CSS style string
    :rtype: str
    """
    return """
    <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
            margin-bottom: 1rem;
            background: #8B4513;
            color: #F5F5DC;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .section-header {
            background: #F5F5DC;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            color: #2F4F4F;
            border: 1px solid #D2B48C;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .white-section {
            background: #F5F5DC;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            color: #2F4F4F;
            border: 1px solid #D2B48C;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
    </style>
    """


def render_page_header(title: str, subtitle: str = "") -> str:
    """
    Render page header with consistent styling.

    :param title: Main title text
    :type title: str
    :param subtitle: Optional subtitle text
    :type subtitle: str
    :return: HTML for page header
    :rtype: str
    """
    subtitle_html = f'<p style="margin: 0; opacity: 0.9;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div class="main-header">
        <h2>{title}</h2>
        {subtitle_html}
    </div>
    """


def render_section_header(title: str) -> str:
    """
    Render section header with consistent styling.

    :param title: Section title text
    :type title: str
    :return: HTML for section header
    :rtype: str
    """
    return f'<div class="section-header">{title}</div>'
