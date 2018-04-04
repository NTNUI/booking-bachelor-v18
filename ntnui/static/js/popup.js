function timeValidate(overlap){
    var formTime = document.getElementById("timeErrorMsg");
    overlap == false;
    if (overlap == false){
        formTime.style.display = "none";
    }else {
        formTime.style.display = "block";
    }
}