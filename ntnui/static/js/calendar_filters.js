// Dropdown for filtering
function dropdownFilters(event){
    var toggleArrow = document.getElementById(event.target.id);
    if ($(toggleArrow).length) {
        toggleArrow.classList.toggle("down");
        var typeId = toggleArrow.nextSibling.nextSibling.id;
        var toggleType = document.getElementById(typeId);
        toggleType.style.display = toggleType.style.display == "block" ? "none" : "block";
    }
}

// Alerts
function triggerFilterAlert(){
    swal({
        title: "Hey!",
        text: "You need to filter on location before seeing the calendar.",
        buttons: false,
        closeOnClickOutside: false
    });
    document.getElementById("top-navbar").style.zIndex="10001";
    document.getElementById("filtering-container").style.borderRadius = "5px";
    $('.filter-cursors').click(function () {
        swal.close();
        document.getElementById("top-navbar").style.zIndex="10";
        document.getElementById("filter-box").style.zIndex="0";
        document.getElementById("filtering-container").style.borderRadius = "0px";
    });
}

// Disable arrow keys from changing the radio buttons
$('input[type="radio"]').keydown(function(e){
    var arrowKeys = [37, 38, 39, 40];
    if (arrowKeys.indexOf(e.which) !== -1){
        $(this).blur();
        var y;
        if (e.which == 38){
            y = $(window).scrollTop();
            $(window).scrollTop(y - 10);
        }else if (e.which == 40){
            y = $(window).scrollTop();
            $(window).scrollTop(y + 10);
        }
        return false;
    }
});

// Removes the calendar blur when filter is used
$('#search-button').click(function (){
    $('#calendar-container').css({
        'pointer-events': 'all',
        '-webkit-filter': 'blur(0px)',
        '-ms-filter': 'blur(0px)',
        'filter': 'blur(0px)'
    })
});

// Removes the calendar blur when filter is used
$('.filter-cursors').click(function (event){
    getLocation(event);
    $('#calendar-container').css({
        'pointer-events': 'all',
        '-webkit-filter': 'blur(0px)',
        '-ms-filter': 'blur(0px)',
        'filter': 'blur(0px)'
    });
});

// Removes the calendar blur when filter is used
$('.type-header').click(function (e){
    dropdownFilters(e);
});