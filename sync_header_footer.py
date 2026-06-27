import re
import sys

def get_block(text, start_marker, end_marker):
    start = text.find(start_marker)
    if start == -1: return ""
    end = text.find(end_marker, start)
    if end == -1: return ""
    return text[start:end + len(end_marker)]

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()
    
    with open('car-detail.html', 'r', encoding='utf-8') as f:
        cd = f.read()

    # Get HTML
    nav_html = get_block(idx, '<nav class="navbar">', '</nav>')
    footer_html = get_block(idx, '<footer class="footer">', '</footer>')
    
    if not nav_html or not footer_html:
        print("Could not find nav or footer in index.html")
        return

    # Replace HTML in car-detail.html
    cd_nav_start = cd.find('<nav class="navbar">')
    cd_nav_end = cd.find('</nav>', cd_nav_start) + 6
    cd = cd[:cd_nav_start] + nav_html + cd[cd_nav_end:]

    cd_footer_start = cd.find('<footer class="footer">')
    cd_footer_end = cd.find('</footer>', cd_footer_start) + 9
    cd = cd[:cd_footer_start] + footer_html + cd[cd_footer_end:]

    # Get CSS
    # CSS for navbar starts with /* NAVBAR */ and ends before /* HERO SECTION */
    css_nav_start = idx.find('/* NAVBAR */')
    css_nav_end = idx.find('/* HERO SECTION */')
    css_nav = idx[css_nav_start:css_nav_end].strip()

    # CSS for footer starts with /* FOOTER */ and ends before #compare-bar or </style>
    css_footer_start = idx.find('/* FOOTER */')
    css_footer_end = idx.find('</style>', css_footer_start)
    
    # We should just take the footer block up to the end of the style tag
    # wait, there's a bunch of 3D carousel stuff. Let's just find the end of footer CSS.
    # Actually, we can just replace the whole navbar and footer CSS in car-detail.html
    css_footer = get_block(idx, '/* FOOTER */', '.fbb-links a:hover {\n      color: var(--white);\n    }')
    
    # Wait, getting the exact CSS is tricky because they share variables.
    # In index.html, root vars:
    root_vars = """
    :root {
      --red: #FFCC00;
      --red-dark: #E6B800;
      --charcoal: #1A3D8F;
      --navy: #0D2B6B;
      --steel: #2A5CC7;
      --silver: #F0F4F8;
      --white: #FFFFFF;
      --text: #1A1A2E;
      --muted: #6B7A99;
      --border: #DDE3EE;
      --success: #A3D1B1;
      --warning: #F59E0B;
      --blue-light: #E8F0FE;
      --primary: #FFCC00;
      --gray-bg: #F3F4F6;
      --blue: #2563EB;
    }
"""

    # In car-detail.html, replace the whole style tag start up to .layout with the combined one
    style_start = cd.find('<style>')
    layout_start = cd.find('.layout { max-width: 1280px;')
    
    if style_start == -1 or layout_start == -1:
        print("Could not find style bounds")
        return
        
    # We can just manually construct the header/footer CSS block
    new_css = """<style>
""" + root_vars + """

    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Inter', sans-serif; color: var(--text); background: var(--gray-bg); }
    a { text-decoration: none; color: inherit; }

""" + css_nav + """

""" + css_footer + """
    .fbb-links a:hover { color: var(--white); }
    
    @media(max-width: 800px) {
      .footer-bottom-bar { flex-direction: column; gap: 16px; border-radius: 16px; text-align: center; }
      .fbb-left { flex-direction: column; gap: 10px; }
      .nav-main { justify-content: space-between; height: 70px; }
      .nav-links, .nav-actions { display: none; }
      .menu-toggle { display: flex; }
    }
    
    .menu-toggle {
      display: none; flex-direction: column; gap: 5px; background: transparent;
      border: none; cursor: pointer; padding: 5px; z-index: 101;
    }
    .menu-toggle span { display: block; width: 25px; height: 3px; background: var(--navy); transition: all 0.3s ease; border-radius: 2px; }

  """
  
    cd = cd[:style_start] + new_css + cd[layout_start:]
    
    with open('car-detail.html', 'w', encoding='utf-8') as f:
        f.write(cd)
    print("Updated car-detail.html")

if __name__ == '__main__':
    main()
