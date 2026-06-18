import re

with open('e:/MarketguruHP/MarketguruHP/MarketguruHP/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

marquee_css = """
  /* SOCIAL MARQUEE */
  .social-marquee-wrapper {
    background: var(--white);
    padding: 16px 0;
    overflow: hidden;
    white-space: nowrap;
    position: relative;
    display: flex;
    align-items: center;
    border-top: 1.5px solid var(--border);
    border-bottom: 1.5px solid var(--border);
  }
  .social-marquee-track {
    display: inline-flex;
    width: max-content;
    animation: marquee-ltr 15s linear infinite;
  }
  /* Pause on hover */
  .social-marquee-wrapper:hover .social-marquee-track {
    animation-play-state: paused;
  }
  .social-marquee-item {
    display: inline-flex;
    align-items: center;
    padding: 0 50px;
  }
  .social-marquee-item a {
    display: inline-flex;
    align-items: center;
    font-size: 20px;
    font-weight: 800;
    color: var(--charcoal);
    text-decoration: none;
    font-family: 'Barlow Condensed', sans-serif;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    transition: color 0.2s;
  }
  .social-marquee-item a:hover {
    color: var(--red-dark);
  }
  .social-marquee-item img {
    height: 32px;
    width: auto;
    margin-left: 12px;
    object-fit: contain;
    vertical-align: middle;
  }

  @keyframes marquee-ltr {
    0% { transform: translateX(-33.3333%); }
    100% { transform: translateX(0%); }
  }
"""

marquee_html = """
<!-- SOCIAL MARQUEE -->
<div class="social-marquee-wrapper">
  <div class="social-marquee-track">
    <!-- Set 1 -->
    <div class="social-marquee-item">
      <a href="https://www.instagram.com/marketguruhp" target="_blank">Follow us on <img src="ig-text.png" alt="Instagram"></a>
    </div>
    <div class="social-marquee-item">
      <a href="https://www.youtube.com/@marketguruhp" target="_blank">Follow us on <img src="yt-text.png" alt="YouTube"></a>
    </div>
    <div class="social-marquee-item">
      <a href="https://www.facebook.com/marketguruhp" target="_blank">Follow us on <img src="fb-text.png" alt="Facebook"></a>
    </div>

    <!-- Set 2 -->
    <div class="social-marquee-item">
      <a href="https://www.instagram.com/marketguruhp" target="_blank">Follow us on <img src="ig-text.png" alt="Instagram"></a>
    </div>
    <div class="social-marquee-item">
      <a href="https://www.youtube.com/@marketguruhp" target="_blank">Follow us on <img src="yt-text.png" alt="YouTube"></a>
    </div>
    <div class="social-marquee-item">
      <a href="https://www.facebook.com/marketguruhp" target="_blank">Follow us on <img src="fb-text.png" alt="Facebook"></a>
    </div>

    <!-- Set 3 -->
    <div class="social-marquee-item">
      <a href="https://www.instagram.com/marketguruhp" target="_blank">Follow us on <img src="ig-text.png" alt="Instagram"></a>
    </div>
    <div class="social-marquee-item">
      <a href="https://www.youtube.com/@marketguruhp" target="_blank">Follow us on <img src="yt-text.png" alt="YouTube"></a>
    </div>
    <div class="social-marquee-item">
      <a href="https://www.facebook.com/marketguruhp" target="_blank">Follow us on <img src="fb-text.png" alt="Facebook"></a>
    </div>
  </div>
</div>

<!-- FEATURED CARS -->"""

# Insert CSS
if '/* SOCIAL MARQUEE */' not in content:
    content = content.replace('</style>', marquee_css + '\n</style>')

# Insert HTML
if '<!-- SOCIAL MARQUEE -->' not in content:
    content = content.replace('<!-- FEATURED CARS -->', marquee_html)

with open('e:/MarketguruHP/MarketguruHP/MarketguruHP/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Marquee added.")
