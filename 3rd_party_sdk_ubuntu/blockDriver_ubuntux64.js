const record=require('node-record-lpcm16');
const aikit=require('./aimakerskitutil');
//const gpio=require('rpi-gpio');
const pIDFinder = require('find-process');
var programArg = require('commander');
//for dht11 sensor
//var sensor = require('node-dht-sensor');
//var PiServo = require('pi-servo');
//var pin2bcm = {3:2, 5:3, 7:4, 8:14, 10:15, 11:17, 12:18, 13:27, 15:22, 16:23, 18:24, 19:10, 21:9, 22:25, 23:11, 24:8, 26:7, 29:5, 31:6, 32:12, 33:13, 35:19, 36:16, 37:26, 38:20, 40:21};
programArg.version(0.1).option("-a,--autorun","from Autorun").parse(process.argv);

if(!programArg.autorun) {
	//if not autorun kill python button_trigger_4share3.py
	var exec = require('child_process').exec;
	exec("sudo systemctl stop aimk_auto");
}else{
	console.log("disable stop python");
}


//node version check
/*
const nodeVersion=process.version.split('.')[0];
let ktkws1=null;


if(nodeVersion==='v6'){
	ktkws1=require('./ktkws');
} else if(nodeVersion==='v8') {
	ktkws1=require('./ktkws_v8');
}
*/

//for playing pcm sound
const Speaker=require('speaker');
const fs=require('fs');
var wav = require('wav');
const soundBuffer=fs.readFileSync('../data/sample_sound.wav');

var genieSpeaker = null;

const client_id='';
const client_key='';
const client_secret='';
const json_path='./key/clientKey.json';
const proto_path='../data/gigagenieRPC.proto';

const kwstext=['기가지니','지니야','친구야','자기야'];
var kwsflag = 0; //=parseInt(process.argv[2]);
const async = require('async')
/*
function initMic(){
        return record.start({
                sampleRateHertz: 16000,
                threshold: 0,
                verbose: false,
                recordProgram: 'arecord',
        })
};
*/
//ktkws1.initialize('../data/kwsmodel.pack');



//let mic=initMic();
var hasKey = false;
if (fs.existsSync(json_path)) {
    // Do something
	hasKey = true;
	aikit.initializeJson(json_path,proto_path);
}
else{
	// 브라우저에 알림 처리
	// 키파일이 등록되지 않음.
}
//aikit.initialize(client_id,client_key,client_secret,cert_path,proto_path);

//기본 GPIO 설정
/*
gpio.setup(29,gpio.DIR_IN,gpio.EDGE_BOTH);//버튼 핀은 입력으로

gpio.on('change',function (channel,value) {
	//29번 핀에 변화가 있는 경우
	if(channel===29 && value === false){
			//console.log("Button Clicked!");
			io.sockets.emit("receiveData",{Type:"ktaimk_button_push",Data:{ret:true}});
			//return;
	}

	io.sockets.emit("receiveData",{Type:"ktaimk_gpio_data",Data:{pin:channel,value:value}});
});
*/
let ozo_timer_id = 0;
var io = require("socket.io").listen(3001);

var device_msg_list = new Array();
class Mutex {
	constructor() {
		this.lock = false; 
	} 
	async acquire() { 
		while (true) { 
			if (this.lock === false) { 
				break; 
			} // custom sleep (setTimeout) 
			await sleep(100); 
		}
		this.lock = true;
	} 
	release() { 
		this.lock = false; 
	} 
}

var dm_buffer = new Array();
let cnt = 0;
const mutex = new Mutex();

io.sockets.on('connection', function(socket) {
		console.log("connect success");
		if(hasKey == false)
		{
			socket.emit("noHasDevKey");
		}
		else {
			socket.emit("hasDevKey");
		}
		socket.on("kill",function() {
			console.log("kill driver");
			socket.emit("die");
			process.exit();
		});
		socket.on("reboot",function() {
			setTimeout(function () {
			    process.on("exit", function () {
			        require("child_process").spawn(process.argv.shift(), process.argv, {
			            cwd: process.cwd(),
			            detached : true,
			            stdio: "inherit"
			        });
			    });
			    process.exit();
			}, 1000);
		});
		socket.on('deviceCtlMsg', async function(msg){
			console.log("---------");
			console.log(msg);
			console.log("---------");
			//await mutex.acquire();
			msg_executor(socket, msg);
			//mutex.release();
			data = getUTCString()
     		console.log(data);
		})
});

var msg_type_list = ["led", "gpioMode", "gpioWrite",  "getDHT11_Temp", "getDHT11_Humidity", "setServo", "bh1750", "dmr", "dmstop", "dma", "setHumanoidMotion", "digitalWrite2", "analogRead", "connect", "disconnect", "move", "on_led", "off_led", "stop", "drive", "rainbow", "flashrainbow", "turnoff", "rotate", "zigzag", "play", "dance"]

async function msg_executor(socket, msg){
// 이 부분에 3rd Party 단말 API를 연동해 주시면 됩니다.
      		if(msg.type == "led")
			{
				ledType = msg.data['type'];
				duration = msg.data['duration'];
				console.log("led on")
				var exec = require('child_process').exec;
				cmd = "python ./ledDriver.py "+ledType+" "+duration;
				exec(cmd,function(error, stdout, stderr) {
				});
			}
};

 const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}
function resolveAfter2Seconds() {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve('resolved');
    }, 2000);
  });
}

let mode=0;//0:idle 1:kws, 2:stt, 3:DSS(QueryVoice)
let ktstt=null;
let ktqbv=null; // DSS (queryByVoice)
/*
mic.on('data',(data)=>{
	if(mode===1){
		result = 0;
		result=ktkws1.pushBuffer(data);
		//result=ktkws2.pushBuffer(data);
		if(result===1) {
			console.log("KWS Detected");
			//pcmplay.write(soundBuffer);
			io.sockets.emit("receiveData",{Type:"ktaimk_kws_detect",Data:{kwsFlag:kwsflag,ret:true}});
			mode = 0;
			//setTimeout(startStt,1000);
		}

	} else if(mode === 2) {
    ktstt.write({audioContent:data});
	} else if(mode === 3) {
		ktqbv.write({audioContent:data});
	}
});
*/


/*
function maruo_waiting_status_check(ret_msg_str){
	//cmd = "python3 ./ozocommand.py "+ "maru_ocheck";
	//result = execShellCommand(cmd);
	var exec = require('child_process').exec;
	cmd = "python3 ./ozocommand.py "+ "maru_ocheck";
	result = exec(cmd,function(error, stdout, stderr) {
	});
	console.log("1 status_check = " + result);
	console.log("1 TimerID = " + ozo_timer_id);
	if(result == 'True' || result =='False'){
		if(ozo_timer_id != null) {
        	clearInterval(ozo_timer_id);
        	socket.emit("receiveData",{Type:ret_msg_str, Data:{wait:result}});
        	ozo_timer_id =null;
    	}
	}
	else if(result =='waiting'){
		console.log("Still waiting.....");
	}
}
*/

function getUTCString(){
	return new Date().toISOString();
}



function execShellCommand(cmd) {
 const exec = require('child_process').exec;
 return new Promise((resolve, reject) => {
 	exec(cmd, (error, stdout, stderr) => {
   	if (error) {
    	console.warn(error);
   	}
   	resolve(stdout? stdout : stderr);
  	});
 	});
}

function playWav(wavData,cb = null){
	var wavReader = new wav.Reader();
	if(genieSpeaker != null)
	{
		//genieSpeaker.close();
	}
	// the "format" event gets emitted at the end of the WAVE header
	wavReader.on('format', function (format) {
		// the WAVE header is stripped from the output of the reader
		genieSpeaker = new Speaker(format);

		genieSpeaker.on("flush",function(){
			if(cb != null)
			{
				cb();
			}
		});
		wavReader.pipe(genieSpeaker);

	});
	wavReader.write(wavData,function(){
		wavReader.end();
	});

}

function startStt(){
	ktstt=aikit.getVoice2Text();
	var stt_data = null;
	ktstt.on('error',(error)=>{
		console.log('Error:'+error);
		io.sockets.emit("receiveData",{Type:"ktaimk_stt_detect",Data:""});
	});
	ktstt.on('data',(data)=>{
		console.log('stt result:'+JSON.stringify(data));
		stt_data = data;
		if(data.resultCd!==200) mode=2;
		if(data.resultCd == 509 ){
			console.log('resOptions resultCd == 509 License limit exceeded');
			io.sockets.emit("receiveData",{Type:"ktaimk_stt_detect",Data:""});
			io.sockets.emit("receiveData",{Type:"ktaimk_license_limit",Data:""});
			return;
		}
	});
	ktstt.on('end',()=>{
        console.log('stt text stream end');
        if(stt_data == null)
        {
            stt_data = "";
		}
		if(stt_data.resultCd == 509 ){
			mode=0;
			return;
		}
		io.sockets.emit("receiveData",{Type:"ktaimk_stt_detect",Data:stt_data});
		mode=0;
	});
	ktstt.write({reqOptions:{mode:0,lang:0}});
	mode=2;
};

function startText2Voice(str,isDSS = false){
	var kttts=aikit.getText2VoiceStream({text:str,lang:0,mode:0});
	kttts.on('error',(error)=>{
		console.log('Error:'+error);
		io.sockets.emit("receiveData",{Type:"ktaimk_tts_finished",Data:str});
	});
	kttts.on('data',(data)=>{
        if(data.streamingResponse==='resOptions' && data.resOptions.resultCd===200) console.log('Stream send. format:'+data.resOptions.format);
        if(data.streamingResponse==='audioContent') {
					//pcmplay.write(data.audioContent);
					playWav(data.audioContent,function(){
						console.log("wav play finish");
						if(isDSS === false)
						{
							io.sockets.emit("receiveData",{Type:"ktaimk_tts_finished",Data:str});
						} else {
							io.sockets.emit("receiveData",{Type:"ktaimk_dss_finished",Data:str});
						}
					});
			}
			else{
				console.log('msg received:'+JSON.stringify(data));
				if(data["resOptions"]["resultCd"] == 500 ){
					console.log('resOptions resultCd == 500 ');
					if(isDSS === false)
					{
						io.sockets.emit("receiveData",{Type:"ktaimk_tts_finished",Data:str});
					} else {
						io.sockets.emit("receiveData",{Type:"ktaimk_dss_finished",Data:str});
					}
				}
				if(data["resOptions"]["resultCd"] == 509 ){
					console.log('resOptions resultCd == 509 License limit exceeded');
					if(isDSS === false)
					{
						io.sockets.emit("receiveData",{Type:"ktaimk_license_limit",Data:""});
						io.sockets.emit("receiveData",{Type:"ktaimk_tts_finished",Data:str});
					} else {
						io.sockets.emit("receiveData",{Type:"ktaimk_license_limit",Data:""});
						io.sockets.emit("receiveData",{Type:"ktaimk_dss_finished",Data:str});
					}

				}
			}
	});
	kttts.on('end',()=>{
		console.log('tts end');
	});
}

function startQueryVoice(){
	ktqbv = aikit.queryByVoice( function(err,msg){
		mode=0; // mic idle mode;
		if(err){
			console.log(JSON.stringify(err));
			io.sockets.emit("receiveData",{Type:"ktaimk_dss_finished",Data:str});

		} else {
			console.log("QueryVoice Msg:"+JSON.stringify(msg));
			const action = msg.action[0];
			const uword = msg.uword;
			if(msg.resultCd == 509 ){
				console.log('resOptions resultCd == 509 License limit exceeded');
				io.sockets.emit("receiveData",{Type:"ktaimk_dss_finished",Data:""});
				io.sockets.emit("receiveData",{Type:"ktaimk_license_limit",Data:""});
				return;
			
			}
			if(action)
			{
				let reqMsgStr = action.mesg;
				//reqMsgStr = striptags(reqMsgStr);
				reqMsgStr = reqMsgStr.replace("<![CDATA[",'');
				reqMsgStr = reqMsgStr.replace(/<[^>]*>/g, '');
				reqMsgStr = reqMsgStr.replace(/\]/gi, '');
				reqMsgStr = reqMsgStr.replace(/\[/gi, '');
				reqMsgStr = reqMsgStr.replace(/\>/gi, '');
				reqMsgStr = reqMsgStr.replace(/\</gi, '');
				console.log(reqMsgStr);
				io.sockets.emit("receiveData",{Type:"ktaimk_stt_detect",Data:uword});
				startText2Voice(reqMsgStr,true);
			}
			else {
				io.sockets.emit("receiveData",{Type:"ktaimk_dss_finished",Data:""});
			}
		}

	});
	//init
	ktqbv.write({reqOptions:{lang:0,userSession:'12345',deviceId:'D06190914TP808IQKtzq'}});
	console.log("Start DSS");
	mode=3;
}

//for devkey
var uploadDir = __dirname+"/key/";
var multer = require('multer');
var upload = multer({
    dest: uploadDir
});

//make dir
fs.mkdir(uploadDir, function() {});

var cors = require('cors');
var http = require('http');
var express = require('express');
var app = express();

// CORS 설정
app.use(cors());

http.createServer(app).listen(3002,function(){
    console.log("http server start");
});

app.post('/upload', upload.single('file'), function(req, res, next) {
	fs.rename(uploadDir + req.file.filename, uploadDir + 'clientKey.json', function() {
			io.sockets.emit('update_complete', "");
			//aikit.initializeJson(json_path,cert_path,proto_path);
    });
})

app.get("/test",function(req,res){
	res.status(200).send("express test");
});
