import asyncio, os, shutil, sys, math
from datetime import datetime
from playwright.async_api import async_playwright

MODE = sys.argv[1]  # desk | mob
FPS = 30
URL = 'http://localhost:8000/index.html?capture'
OUT = f'capture/frames_{MODE}'
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
n = 0

def ease(t):  # easeInOutCubic
    return 4*t*t*t if t < .5 else 1 - pow(-2*t+2, 3)/2

async def main():
    global n
    async with async_playwright() as p:
        b = await p.chromium.launch()
        if MODE == 'desk':
            ctx = await b.new_context(viewport={'width':1920,'height':1080}, device_scale_factor=1, timezone_id='Europe/London')
        else:
            ctx = await b.new_context(viewport={'width':390,'height':693}, device_scale_factor=1080/390, is_mobile=True, has_touch=True, timezone_id='Europe/London')
        pg = await ctx.new_page()
        await pg.clock.install(time=datetime(2026,10,2,19,0,0))
        await pg.goto(URL);
        await pg.evaluate('document.fonts.ready')
        await pg.add_style_tag(content='''
          .mobile-menu,.dock,.site-head{transition:none!important}
          #endcard{position:fixed;inset:0;z-index:999;background:#0F1620;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:0;pointer-events:none;padding:24px}
          #endcard b{font-family:"Big Shoulders Display";font-weight:900;font-size:clamp(72px,12vw,160px);line-height:.9;text-transform:uppercase;color:#F3EEE4}
          #endcard i{font-style:normal;font-family:"Big Shoulders Display";font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#F2A541;font-size:clamp(22px,2.4vw,34px)}
          #endcard p{font-family:Figtree;color:#C9C4BB;font-size:clamp(17px,1.5vw,22px);margin:28px 0 0;max-width:none}
          #endcard .s{margin-top:34px;padding:12px 22px;border:2px solid #F2A541;border-radius:12px;font-family:"Big Shoulders Display";font-weight:900;font-size:clamp(28px,3vw,40px);color:#FFD9A0;text-transform:uppercase;text-shadow:0 0 6px rgba(242,165,65,.9),0 0 22px rgba(242,165,65,.6);box-shadow:0 0 30px rgba(242,165,65,.35)}
        ''')
        await pg.evaluate('''()=>{const d=document.createElement('div');d.id='endcard';d.innerHTML='<b>Unity</b><i>Barbers</i><p>166 Alfreton Road, Radford, Nottingham</p><div class="s">Open till 11, 7 days</div>';document.body.appendChild(d);}''')
        print('styled',flush=True)
        await pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
        H = await pg.evaluate('document.documentElement.scrollHeight')
        for y in range(0, H, 400):
            await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(40)
        await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(800)
        print('scrolled',flush=True)
        await pg.evaluate("document.getElementById('head').classList.remove('solid'); dispatchEvent(new Event('scroll'))")

        async def shot():
            global n
            await pg.screenshot(path=f'{OUT}/f{n:05d}.jpg', type='jpeg', quality=93)
            n += 1
        async def hold(sec):
            global n
            await shot(); src = f'{OUT}/f{n-1:05d}.jpg'
            for _ in range(int(sec*FPS)-1):
                shutil.copy(src, f'{OUT}/f{n:05d}.jpg'); n += 1
        async def scroll_to(target, sec):
            y0 = await pg.evaluate('scrollY')
            maxy = await pg.evaluate('document.documentElement.scrollHeight - innerHeight')
            y1 = max(0, min(target, maxy))
            k = int(sec*FPS)
            for i in range(1, k+1):
                y = y0 + (y1-y0)*ease(i/k)
                await pg.evaluate(f'scrollTo(0,{y}); dispatchEvent(new Event("scroll"))')
                await shot()
        async def top_of(sel, offset):
            return await pg.evaluate(f'document.querySelector("{sel}").getBoundingClientRect().top + scrollY') - offset
        async def anim(js_tpl, sec):
            k = int(sec*FPS)
            for i in range(1, k+1):
                await pg.evaluate(js_tpl.replace('T', str(ease(i/k))))
                await shot()

        print('ready',flush=True)
        flick = [0,0,0,1,1,.2,.2,1,1,1,.4,1,1,1,1]
        for o in flick:
            await pg.evaluate(f'document.querySelector(".sign .big").style.opacity={o}')
            await shot()
        await hold(2.4)

        if MODE == 'mob':
            await pg.evaluate("const m=document.getElementById('mmenu');m.style.visibility='visible';m.style.transform='translateY(-100%)'")
            await anim("document.getElementById('mmenu').style.transform='translateY('+(-100+100*T)+'%)'", .5)
            await hold(1.4)
            await anim("document.getElementById('mmenu').style.transform='translateY('+(-100*T)+'%)'", .45)
            await pg.evaluate("const m=document.getElementById('mmenu');m.style.visibility='';m.style.transform=''")
            await hold(.4)

        off = 72 if MODE == 'desk' else 60
        vh = 1080 if MODE == 'desk' else 693
        stops = []
        stops.append((await top_of('#hair', off) , 1.6, 1.4))
        stops.append((await top_of('.tex-grid', off+12), 1.3, 1.8))
        stops.append((await top_of('#hours', off - (0 if MODE=='desk' else 0)) + (0 if MODE=='desk' else 0), 1.6, 2.0))
        if MODE == 'mob':
            stops.append((await top_of('#hours h2', off+20), 1.2, 1.4))
        stops.append((await top_of('#prices', off), 1.6, 1.6))
        stops.append((await top_of('#menu', off+20), 1.2, 2.2))
        if MODE == 'mob':
            stops.append((await top_of('#menu .menu-group:nth-child(2)', off+20), 1.2, 1.6))
        stops.append((await top_of('.perks', off+40), 1.3, 1.6))
        for y, s, h in stops:
            await scroll_to(y, s); await hold(h)

        # gallery
        await scroll_to(await top_of('#work', off), 1.6); await hold(1.2)
        await scroll_to(await top_of('#gallery', off+16), 1.2); await hold(1.2)
        await pg.evaluate('window.__lb.openLb(1)'); await hold(1.3)
        await pg.evaluate('window.__lb.show(2)'); await hold(1.1)
        await pg.evaluate('window.__lb.show(3)'); await hold(1.1)
        await pg.evaluate('window.__lb.closeLb()'); await hold(.5)
        if MODE == 'mob':
            await scroll_to(await top_of('#gallery button:nth-child(8)', off+16), 1.4); await hold(1.0)
        else:
            await scroll_to(await top_of('#gallery', off+16) + vh*0.55, 1.4); await hold(1.0)

        # find us + final
        await scroll_to(await top_of('#find', off + (40 if MODE=='desk' else 0)), 1.6); await hold(2.2)
        if MODE == 'mob':
            await scroll_to(await top_of('.map', off+40), 1.2); await hold(1.6)
        await scroll_to(await top_of('.final', off), 1.6); await hold(2.2)
        await scroll_to(10**6, 1.2); await hold(1.0)

        # end card
        await anim("document.getElementById('endcard').style.opacity=T", .8)
        await hold(3.0)
        await b.close()
    print('frames', n)

asyncio.run(main())
