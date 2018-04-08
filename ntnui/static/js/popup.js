//function overlapValidate(overlap){
//    var formTime = document.getElementById("timeErrorMsg");
//    overlap == false;
//    if (overlap == false){
//        formTime.style.display = "none";
//    }else {
//        formTime.style.display = "block";
//    }
//}
//
function lengthValidate(){
  var errorMsg = document.getElementById("timeErrorMsg");
  var startTime = document.getElementById("startInput").value;
  var endTime = document.getElementById("endInput").value;
  var arrStart = startTime.split(':'), hourStart = arrStart[0], minStart = arrStart[1];
  var arrEnd = endTime.split(':'), hourEnd = arrEnd[0], minEnd = arrEnd[1];
  console.log(hourStart, hourEnd, minStart, minEnd);
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
  else{
    errorMsg.style.display = "none";
    return true;
  }
}

function editClock(){
  var clockTicks = document.getElementsByClassName('clockpicker-tick');
  var startTime = document.getElementById('startInput');
  var startHour = startTime.value.substring(0,2);
  var startMinute = startTime.value.substring(3,5);
  var hourParent = clockTicks[0].parentNode.className;
  console.log(startHour, startMinute);
  for(var i=0;i<clockTicks.length; i++){
    console.log(clockTicks[i].parentNode.className);
    if((clockTicks[i].innerHTML < startHour || clockTicks[i].innerHTML<10) && (i>36 && i<60))  {
        clockTicks[i].style.color = "#DCDCDC";
        clockTicks[i].style.pointerEvents = "none";
    }
    //if((i != 41||46||51||56) && (clockTicks[i].innerHTML < startMinute && i>60)){
    //    clockTicks[i].style.color = "#DCDCDC";
    //    clockTicks[i].style.pointerEvents = "none";
    //}
    if((clockTicks[i].innerHTML >= startHour) && (i>45 && i<60)){
        clockTicks[i].style.color = "black";
        clockTicks[i].style.pointerEvents = "auto";
    }
    
  }
}

function editClockMinutes(){
  var clockTicks = document.getElementsByClassName('clockpicker-tick');
  var startTime = document.getElementById('startInput');
  var startHour = startTime.value.substring(0,2);
  var startMinute = startTime.value.substring(3,5);
  var endTime = document.getElementById('endInput');
  var endHour = endTime.value.substring(0,2);
  console.log(endHour, startHour);
  if(startHour == endHour && startMinute>0){
    for(var i=0;i<clockTicks.length; i++){
      if(clockTicks[i].innerHTML <= startMinute && i>60 && (i != 41||46||51||56)){
        clockTicks[i].style.color = "#DCDCDC";
        clockTicks[i].style.pointerEvents = "none";
      }
    }
  }
  if(startHour != endHour || startMinute==0){
    for(var i=0;i<clockTicks.length; i++){
      if(i>60){
        clockTicks[i].style.color = "black";
        clockTicks[i].style.pointerEvents = "auto";
      }
    }
  }
}


