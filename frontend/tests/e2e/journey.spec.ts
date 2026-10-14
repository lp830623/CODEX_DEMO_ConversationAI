import {test,expect} from '@playwright/test';
test('complete synthetic demo journey',async({page})=>{
 await page.goto('/');await expect(page.getByText('Lokalne API',{exact:true})).toBeVisible();
 await page.getByRole('button',{name:'Resetuj demo',exact:true}).click();
 await page.getByRole('button',{name:'Otwórz CALL-001',exact:true}).click();
 await expect(page.getByRole('dialog')).toContainText('Quality Score');
 await page.getByRole('button',{name:'Transkrypcja · 7',exact:true}).click();
 await expect(page.getByRole('dialog')).toContainText('oddzwonię jutro do godziny 14:00');
 const audio=page.locator('audio');await audio.evaluate((a:HTMLAudioElement)=>{a.load();});
 await expect.poll(()=>audio.evaluate((a:HTMLAudioElement)=>a.readyState)).toBeGreaterThan(0);
 expect(await audio.evaluate((a:HTMLAudioElement)=>a.duration)).toBeGreaterThan(90);
 await page.getByRole('button',{name:'Zamknij szczegóły'}).click();
 await page.getByRole('button',{name:'Promise Tracker',exact:true}).click();
 await page.getByLabel('Termin deklaracji',{exact:true}).selectOption('missing');
 await expect(page.getByText('Nie podano',{exact:true}).first()).toBeVisible();
 await page.setViewportSize({width:390,height:844});
 await expect(page.getByRole('navigation')).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBeTruthy();
});
