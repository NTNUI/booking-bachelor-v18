// Validates the input of the timepicker.

function validateTime(){
    var errorMsg = document.getElementById("timeErrorMsg");
    var startTime = document.getElementById("startInput").value;
    var endTime = document.getElementById("endInput").value;
    var arrStart = startTime.split(':'), hourStart = arrStart[0], minStart = arrStart[1];
    var arrEnd = endTime.split(':'), hourEnd = arrEnd[0], minEnd = arrEnd[1];
    if((hourEnd < hourStart) || (hourEnd == hourStart && minStart > minEnd)){
        alert("End can't be before start");
        //errorMsg.style.display = "block";
        return false;
    }if(hourEnd==hourStart && (minEnd - minStart)<30){
        alert('Minimum 30 minutes')
        //errorMsg.innerHTML == "The appointment must be atleast 30 minutes";
        //errorMsg.style.display = "block";
        return false;
    }if((hourEnd-hourStart)>3){
        alert('Maximum 3 hours');
        //errorMsg.innerHTML = "Maximum 3 hours";
        //errorMsg.style.display = "block";
        return false;
    }
    //if(busyHours.contains(startHour) || busyHours.contains(hourEnd)){
    //    alert('That hour is busy');
    //    //errorMsg.innerHTML = "That hour is busy";
    //    //errorMsg.style.display = "block";
    //    return false;
    //}
    else{
        //errorMsg.style.display = "none";
        return true;
    }
}

// Resets both timers if the user wants to change starttime
function resetClock(){
    var clockTicks = document.getElementsByClassName('clockpicker-tick');
    var endTime = document.getElementById('endInput');
    for(var i=0;i<clockTicks.length; i++){
        if(clockTicks.length == 28)
            if(clockTicks[i].innerHTML > 10 && clockTicks[i].innerHTML < 23 || (clockTicks[i].innerHTML == '00' && i>(+clockTicks.length - 4))){
                clockTicks[i].style.color = "black";
                clockTicks[i].style.pointerEvents = "auto";
                endTime.value = 'Choose end time';
                endTime.disabled = true;
            }
        if(clockTicks.length == 56){
            if(clockTicks[i].innerHTML > 10 && clockTicks[i].innerHTML < 23 || (clockTicks[i].innerHTML == '00' && i>(+clockTicks.length - 36   ))){
                clockTicks[i].style.color = "black";
                clockTicks[i].style.pointerEvents = "auto";
                endTime.value = 'Choose end time';
                endTime.disabled = true;
            }
        }
    }
}

// Edits the clockpicker so that invalid times cant be picked.
function editClock(){
    var clockTicks = document.getElementsByClassName('clockpicker-tick');
    var startTime = document.getElementById('startInput');
    var endTime = document.getElementById('endInput');
    var startHour = startTime.value.substring(0,2);
    var startMinute = startTime.value.substring(3,5);
    var hourParent = clockTicks[0].parentNode.className;
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

// Checks if starttime is picked before endtime is able to be picked
function checkStartTime(){
    var startTime = document.getElementById('startInput');
    var endTime = document.getElementById('endInput');
    var endTimeSpan = document.getElementById('endTimeSpan');
    if(startTime.value == 'Choose start time'){
        endTime.disabled = true;
        endTimeSpan.style.pointerEvents = "none";
    }if(startTime.value != 'Choose start time'){
        endTime.disabled = false;
        endTimeSpan.style.pointerEvents = "auto";
    }

}

// Edits minimum date and maximum date of the timepicker. Stops at the end of the semester
function minMaxDate(){
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1;
    var yyyy = today.getFullYear();
        if(dd<10){
            dd='0'+dd
        }
        if(mm<10){
            mm='0'+mm
        }
    today = yyyy+'-'+mm+'-'+dd;
    var maxdd;
    var maxmm;
    if(mm <= 6){
        maxmm = '0'+6;
        maxdd = 10;
    }
    if(mm >= 8){
        maxmm = 12;
        maxdd = 21;
    }
    var maxDate = yyyy+'-'+maxmm+'-'+maxdd;
    document.getElementById('datefield').setAttribute('min', today);
    document.getElementById('datefield').setAttribute('max', maxDate);
}

