const puppeteer = require('puppeteer-core');

if(process.argv.length != 3){
    console.log("자동실행할 gen파일의 주소를 입력해주세요.");
}

var filePath = process.argv[2];

(async () => { 
    function delay(timeout) {
    return new Promise((resolve) => {
        setTimeout(resolve, timeout);
    });
    }
    console.log("launch!");
    const browser = await puppeteer.launch({
        headless : true,
        devtools: false,
        ignoreHTTPSErrors: true,
        // 윈도우 크롬 자동 설치시 설치되는 경로
        executablePath : "/usr/bin/chromium-browser",
        // 실행될 브라우저의 화면 크기를 지정한다.
        defaultViewport : { width : 1024, height: 768 },
      //args : [ ]
    });
    console.log("new page");
    browser.newPage().then(async (page)=> {
        console.log("goto page");
        page.on('console', async function(msg) {
            console.log('PAGE LOG:', msg.text());
            if(msg.text() == "finish runCode"){
                console.log("Finish Auto run");
                console.log("get screenshot!");
                await page.screenshot({path: './screenshot.png'});
                browser.close();
            }
        });
        await page.goto('https://genieblock.kt.co.kr/block',{waitUntil: 'load', timeout: 0});
        
        console.log("prepare autorun");
        await page.evaluate(function() {
            Killdos.preprocessAutorun();
        });

        console.log("set upload file");
        const input = await page.$("#CodeUpload");
        await input.uploadFile(filePath);
        await delay(2000);
        console.log("runCode!");
        await page.evaluate(function() {
            Killdos.runCode();
        });
        
        
        
        //await delay(5000);
        
    });
    
})();
