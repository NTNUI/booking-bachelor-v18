function validateTime(busyHours){
    var errorMsg = document.getElementById("timeErrorMsg");
    var startTime = document.getElementById("startInput").value;
    var endTime = document.getElementById("endInput").value;
    var arrStart = startTime.split(':'), hourStart = arrStart[0], minStart = arrStart[1];
    var arrEnd = endTime.split(':'), hourEnd = arrEnd[0], minEnd = arrEnd[1];
    if((hourEnd < hourStart) || (hourEnd == hourStart && minStart > minEnd)){
        errorMsg.innerHTML = "End can't be before start";
        errorMsg.style.display = "block";
        return false;
    }if(hourEnd-hourStart == 0 && (minEnd - minStart)<30){
        errorMsg.innerHTML == "The appointment must be atleast 30 minutes";
        errorMsg.style.display = "block";
        return false;
    }if((hourEnd-hourStart)>3){
        errorMsg.innerHTML = "Maximum 3 hours";
        errorMsg.style.display = "block";
        return false;
    }
    if(busyHours.contains(startHour) || busyHours.contains(hourEnd)){
        errorMsg.innerHTML = "That hour is busy";
        errorMsg.style.display = "block";
        return false;
    }
    else{
        errorMsg.style.display = "none";
        return true;
    }
}
function resetClock(){
    console.log("test");
    var clockTicks = document.getElementsByClassName('clockpicker-tick');
    var endTime = document.getElementById('endInput');
    for(var i=0;i<clockTicks.length; i++){
        if((clockTicks[i].innerHTML > 10 && clockTicks[i].innerHTML < 23 || clockTicks.innerHTML == '00') && i<(+clockTicks.length - 4)){
            clockTicks[i].style.color = "black";
            clockTicks[i].style.pointerEvents = "auto";
            endTime.value = 'Choose end time';
            endTime.disabled = true;
        }

    }
}


function editClock(){
    var clockTicks = document.getElementsByClassName('clockpicker-tick');
    var startTime = document.getElementById('startInput');
    var endTime = document.getElementById('endInput');
    var startHour = startTime.value.substring(0,2);
    var startMinute = startTime.value.substring(3,5);
    var hourParent = clockTicks[0].parentNode.className;
    console.log("editing clock", startHour);
    for(var i=0;i<clockTicks.length; i++){
        if((clockTicks[i].innerHTML < +startHour+1 || clockTicks[i].innerHTML<10) && i<(+clockTicks.length - 4))  {
            clockTicks[i].style.color = "#DCDCDC";
            clockTicks[i].style.pointerEvents = "none";
        }
        //if((i != 41||46||51||56) && (clockTicks[i].innerHTML < startMinute && i>60)){
        //    clockTicks[i].style.color = "#DCDCDC";
        //    clockTicks[i].style.pointerEvents = "none";
        //}
    }


}

function checkStartTime(){
    var startTime = document.getElementById('startInput');
    var endTime = document.getElementById('endInput');
    if(startTime.value == 'Choose start time'){
        endTime.disabled = true;
    }if(startTime.value != 'Choose start time'){
        endTime.disabled = false;
    }

}

