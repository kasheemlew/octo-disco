from pyppeteer import launch


async def crawl(url, xpaths):
    print('crawl')
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport(viewport={'width': 1280, 'height': 800})
    await page.setJavaScriptEnabled(enabled=True)
    await page.goto(url)
    for xpath in xpaths:
        elms = await page.xpath(xpath)
        for elm in elms:
            content = await (await elm.getProperty('textContent')).jsonValue()
            print(await elm.getProperty('textContent'))
            print(content)
    await browser.close()
