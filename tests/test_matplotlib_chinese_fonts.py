#!/usr/bin/env python
"""
# OS install chinese fonts.
sudo apt install fonts-wqy-microhei fonts-wqy-zenhei fonts-noto-cjk

# Clear fonts cache
rm -rf ~/.cache/matplotlib

# Find chinese fonts
fc-list : family | grep -i "Noto Sans CJK SC|WenQuanYi|Hei"

# Create font config if not exist
python -c "import matplotlib; print(matplotlib.matplotlib_fname())"

# Editor font config, default at ~/.config/matplotlib/matplotlibrc
vi ~/.config/matplotlib/matplotlibrc
  font.family        : sans-serif
  font.sans-serif    : /home/kasm-user/.fonts/truetype/wqy-microhei.ttc, WenQuanYi Zen Hei, Noto Sans CJK SC, DejaVu Sans, sans-serif
  axes.unicode_minus : False
"""

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = os.path.expanduser('~/.fonts/truetype/wqy-microhei.ttc')
fm.fontManager.addfont(font_path)
font_prop = fm.FontProperties(fname=font_path)
print(f"Loaded chinese fonts: {font_prop.get_name()}")

for font in fm.fontManager.ttflist:
    if 'han sans' in font.name.lower() or 'sans cjk' in font.name.lower() or 'wenquanyi' in font.name.lower():
        print(f"Font Name: {font.name}")
        print(f"Font Path: {font.fname}")
        print("-" * 50)

chinese_font = 'WenQuanYi Micro Hei'

# Setting Global Fonts
plt.rcParams['font.sans-serif'] = [chinese_font,]
plt.rcParams['axes.unicode_minus'] = False  # Solve the negative sign display issue

# Test Drawing
plt.plot([1, 2, 3], label='测试曲线')
plt.title('中文标题示例')
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.show()

# Save image to /tmp/tmp.png
plt.savefig('/tmp/tmp.png', dpi=100, bbox_inches='tight')
plt.close()

# Manual setting fonts path.
font_path = '/home/kasm-user/.fonts/truetype/wqy-microhei.ttc'
font_prop = fm.FontProperties(fname=font_path)
plt.title('中文标题', fontproperties=font_prop)
plt.show()
plt.savefig('/tmp/tmpx.png', dpi=100, bbox_inches='tight')
plt.close()
