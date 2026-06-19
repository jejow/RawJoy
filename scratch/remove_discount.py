import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    modified = False

    # 1. db-bridge.js modifications
    if filepath.endswith('db-bridge.js'):
        replacements = [
            (
                'const isBundleEligible = uniqueBundleItems.length >= 3;',
                'const isBundleEligible = false;'
            ),
            (
                'if (isBundleEligible && bundleProducts.indexOf(slug) !== -1)',
                'if (false && bundleProducts.indexOf(slug) !== -1)'
            ),
            (
                'const uniqueProductCount = uniqueBundleItems.length;',
                'const uniqueProductCount = 0;'
            ),
            (
                'const isBundleEligible = uniqueProductCount >= 3;',
                'const isBundleEligible = false;'
            ),
            (
                'const discountAmount = isBundleEligible ? originalBundleTotal * 0.15 : 0;',
                'const discountAmount = 0;'
            ),
            (
                '// Bundle discount logic: 3+ unique bundle products = 15% OFF those products',
                '// Bundle logic'
            ),
            (
                '🎁 Bundle -15%',
                '🎁 Bundle'
            ),
            (
                'to get <strong>15% OFF</strong> those products!',
                'to get them!'
            ),
            (
                'to get <strong>15% OFF</strong> those products!</span>',
                'to get them!</span>'
            ),
            (
                '3+ products = 15% OFF · You save',
                '3+ products'
            ),
            (
                '3+ products = 15% OFF',
                '3+ products'
            )
        ]
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                modified = True

        # Remove HTML templates using regex
        p1 = re.compile(r'\$\{!isEmpty\s*&&\s*isBundleEligible\s*\?[\s\S]*?:\s*\'\'\s*\}')
        if p1.search(content):
            content = p1.sub("''", content)
            modified = True

        p2 = re.compile(r'\$\{!isEmpty\s*&&\s*!isBundleEligible\s*&&\s*uniqueProductCount\s*>\s*0\s*\?[\s\S]*?:\s*\'\'\s*\}')
        if p2.search(content):
            content = p2.sub("''", content)
            modified = True

        p3 = re.compile(r'\$\{isBundleEligible\s*\?[\s\S]*?:\s*`[\s\S]*?footer-total-price">[\s\S]*?`\s*\}')
        if p3.search(content):
            content = p3.sub('`<div class="footer-total-price">${totalStr}</div>`', content)
            modified = True

    # 2. cart-interceptor.js modifications
    if filepath.endswith('cart-interceptor.js'):
        replacements = [
            (
                'var isBundleEligible = uniqueBundleItems.length >= 3;',
                'var isBundleEligible = false;'
            ),
            (
                'if (isBundleEligible && bundleProducts.indexOf(slug) !== -1)',
                'if (false && bundleProducts.indexOf(slug) !== -1)'
            ),
            (
                'var uniqueProductCount = uniqueBundleItems.length;',
                'var uniqueProductCount = 0;'
            ),
            (
                'var isBundleEligible = uniqueProductCount >= 3;',
                'var isBundleEligible = false;'
            ),
            (
                'var discountAmount = isBundleEligible ? originalBundleTotal * 0.15 : 0;',
                'var discountAmount = 0;'
            ),
            (
                '// Bundle discount logic: 3+ unique bundle products = 15% OFF those products',
                '// Bundle logic'
            ),
            (
                '🎁 Bundle -15%',
                '🎁 Bundle'
            ),
            (
                'to get <strong>15% OFF</strong> those products!',
                'to get them!'
            ),
            (
                'to get <strong>15% OFF</strong> those products!</span>',
                'to get them!</span>'
            ),
            (
                '3+ products = 15% OFF · You save',
                '3+ products'
            ),
            (
                '3+ products = 15% OFF',
                '3+ products'
            )
        ]
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                modified = True

        # Remove HTML templates using regex in cart-interceptor
        p1 = re.compile(r'\(!isEmpty\s*&&\s*isBundleEligible\s*\?[\s\S]*?:\s*\'\'\s*\)\s*\+\s*')
        if p1.search(content):
            content = p1.sub("'' + ", content)
            modified = True

        p2 = re.compile(r'\(!isEmpty\s*&&\s*!isBundleEligible\s*&&\s*uniqueProductCount\s*>\s*0\s*\?[\s\S]*?:\s*\'\'\s*\)\s*\+\s*')
        if p2.search(content):
            content = p2.sub("'' + ", content)
            modified = True

        p3 = re.compile(r'\(isBundleEligible\s*\?[\s\S]*?:\s*\'\s*<div class="footer-total-price">\'\s*\+\s*totalStr\s*\+\s*\'</div>\'\s*\)')
        if p3.search(content):
            content = p3.sub("'      <div class=\"footer-total-price\">' + totalStr + '</div>'", content)
            modified = True

    # 3. cart/index.html specific modifications
    if 'cart' in filepath and filepath.endswith('index.html') and 'checkout' not in filepath:
        # In getDirectLocalCart
        replacements = [
            (
                'const isBundleEligible = uniqueBundleItems.length >= 3;',
                'const isBundleEligible = false;'
            ),
            (
                'if (isBundleEligible && bundleProducts.indexOf(slug) !== -1) {',
                'if (false) {'
            ),
            (
                'const isBundleEligible = uniqueBundleItems.length >= 3;\n    const discountAmount = isBundleEligible ? originalBundleTotal * 0.15 : 0;\n    const originalTotal = originalBundleTotal + originalNonBundleTotal;\n    const finalTotal = originalTotal - discountAmount;',
                'const isBundleEligible = false;\n    const discountAmount = 0;\n    const originalTotal = originalBundleTotal + originalNonBundleTotal;\n    const finalTotal = originalTotal;'
            ),
            (
                'const isBundleEligible = false;\n    const discountAmount = isBundleEligible ? originalBundleTotal * 0.15 : 0;\n    const originalTotal = originalBundleTotal + originalNonBundleTotal;\n    const finalTotal = originalTotal - discountAmount;',
                'const isBundleEligible = false;\n    const discountAmount = 0;\n    const originalTotal = originalBundleTotal + originalNonBundleTotal;\n    const finalTotal = originalTotal;'
            )
        ]
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                modified = True

        # Let's also do a replacement of the summaryEl innerHTML discount block
        p_disc = re.compile(r'\$\{isBundleEligible\s*\?[\s\S]*?:\s*uniqueBundleItems.length\s*>\s*0\s*\?[\s\S]*?:\s*\'\'\s*\}')
        if p_disc.search(content):
            content = p_disc.sub("''", content)
            modified = True

        p_row = re.compile(r'\$\{isBundleEligible\s*\?[\s\S]*?:\s*\'\'\s*\}')
        if p_row.search(content):
            content = p_row.sub("''", content)
            modified = True

    # 4. pages/checkout/index.html specific modifications
    if 'checkout' in filepath and filepath.endswith('index.html'):
        replacements = [
            (
                'const isBundleEligible = uniqueProductCount >= 3;',
                'const isBundleEligible = false;'
            ),
            (
                'const discountAmount = isBundleEligible ? originalBundleTotal * 0.15 : 0;',
                'const discountAmount = 0;'
            ),
            (
                'const finalTotal = originalTotal - discountAmount;',
                'const finalTotal = originalTotal;'
            ),
            (
                '<span>Bundle Discount (15%)</span>',
                '<span>Bundle Discount</span>'
            ),
            (
                '🎁 Bundle -15%',
                '🎁 Bundle'
            )
        ]
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                modified = True

    # 5. General HTML promotional text replacements
    if filepath.endswith('.html'):
        replacements = [
            (
                'Build your bundle get 15% OFF',
                'Build your custom bundle'
            ),
            (
                'Choose any 3 products and get 15% OFF your total. Build your bundle today.',
                'Choose any 3 products to build your custom bundle today.'
            )
        ]
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated: {filepath}')

if __name__ == '__main__':
    for root, dirs, files in os.walk('.'):
        if any(k in root for k in ['node_modules', '.git', '.gemini']):
            continue
        for f in files:
            if f.endswith('.html') or f.endswith('.js'):
                process_file(os.path.join(root, f))
