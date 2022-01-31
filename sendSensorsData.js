#!/usr/bin/zsh

const execSync = require("child_process").execSync;
const fs = require("fs");
const spawn = require("child_process").spawn;

let commandObject = {
    "sensor":"sensors -Aj"
}

let commandOutput = {};

commandOutput[Object.keys(commandObject)[0]] = JSON.parse(execSync(commandObject.sensor));


let sensorInfo = {}
if(commandOutput["sensor"]["iwlwifi_1-virtual-0"]){
    sensorInfo["wifi-chip-temp"] = commandOutput["sensor"]["iwlwifi_1-virtual-0"]["temp1"]["temp1_input"];
}
if(commandOutput["sensor"]["nvme-pci-0600"]){
    sensorInfo["ssd-composite-temp"] = commandOutput["sensor"]["nvme-pci-0600"]["Composite"]["temp1_input"];
    sensorInfo["ssd-sensor1-temp"] = commandOutput["sensor"]["nvme-pci-0600"]["Sensor 1"]["temp2_input"];
    sensorInfo["ssd-sensor2-temp"] = commandOutput["sensor"]["nvme-pci-0600"]["Sensor 2"]["temp3_input"];
}
if(commandOutput["sensor"]["coretemp-isa-0000"]){
    sensorInfo["cpu-0-temp"] = commandOutput["sensor"]["coretemp-isa-0000"]["Core 0"]["temp2_input"];
    sensorInfo["cpu-1-temp"] = commandOutput["sensor"]["coretemp-isa-0000"]["Core 1"]["temp3_input"];
    sensorInfo["cpu-2-temp"] = commandOutput["sensor"]["coretemp-isa-0000"]["Core 2"]["temp4_input"];
    sensorInfo["cpu-2-temp"] = commandOutput["sensor"]["coretemp-isa-0000"]["Core 3"]["temp5_input"];
}

console.log(sensorInfo)

fs.writeFile("sensors.json", JSON.stringify(sensorInfo,undefined,2),() => {
    console.log("starting upload routine...\n")
    const uploader = spawn("python3",["/home/plusx/sendSensorData/uploadToGoogleSheets.py"]);
    uploader.stderr.on("err",(err) => {
        console.log("err: ",err);
    });

    uploader.stdout.on('msg',(msg)=>{
        console.log("msg: ",msg);
    });
});
