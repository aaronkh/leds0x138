const express = require('express')
const app = express()
const port = 3000
app.use(express.json())
app.use(express.static('./'))
let stats = {red:255, blue:255, green:255}
const Gpio = require('pigpio').Gpio;

const red = new Gpio(3, {mode: Gpio.OUTPUT})
const green = new Gpio(2, {mode: Gpio.OUTPUT})
const blue = new Gpio(4, {mode: Gpio.OUTPUT})

/**********
* Primary LED RGB control
**********/

app.post('/red', function(req, res){
	stats.red = req.body.brightness
	red.pwmWrite(req.body.brightness)
	res.status(200)
	.send()
})

app.post('/green', function(req, res){
	console.log(req.body)
	stats.green = (req.body.brightness)
	green.pwmWrite(req.body.brightness)
	res.status(200)
	.send()
})


app.post('/blue', function(req, res){
	stats.blue = req.body.brightness
	blue.pwmWrite(req.body.brightness)
	res.status(200)
	.send()
})

// combined endpoint for red green and blue
app.post('/rgb', function(req, res){
	console.log(req.body)
	if(req.body.red != undefined){
		stats.red = req.body.red
		red.pwmWrite(req.body.red)
	}
	if(req.body.green != undefined){
		stats.green = req.body.green
		green.pwmWrite(req.body.green)
	}
	if(req.body.blue != undefined){
		stats.blue = req.body.blue
		blue.pwmWrite(req.body.blue)
	}
	res.status(200).send()
})


/**********
* Additional Functionality
**********/

// use /stats as redirect uri
app.get('/stats', function(req, res){
	if(req.query.code) auth_code = req.query.code
	res.send(stats)
})

// this server can be used to catch redirected auth codes
let auth_code = ''
app.get('/auth_code', (req, res) => {
	if(auth_code) res.send(auth_code)
	res.send(500, {error: 'auth_code already sent, try requesting another?'})
})

/**********
* Start HTTP server
**********/

app.listen(port, 
	function(){
		red.pwmWrite(255)
		blue.pwmWrite(255)
		green.pwmWrite(255)	
		console.log(`now listening on port ${port}`)
	})

app.listen(80, function(){console.log('also listening on 80')})
