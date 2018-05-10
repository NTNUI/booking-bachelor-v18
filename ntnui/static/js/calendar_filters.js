// Dropdown for filtering
function dropdownFilters(event){
    var toggleArrow = document.getElementById(event.target.id);
    toggleArrow.classList.toggle("down");
    var typeId = toggleArrow.nextSibling.nextSibling.id;
    var toggleType = document.getElementById(typeId);
    toggleType.style.display = toggleType.style.display == "block" ? "none" : "block";
};

// Alerts
function triggerFilterAlert(){
    swal({
        title: "Hey!",
        text: "You need to filter on location before seeing the calendar.",
        buttons: false,
        closeOnClickOutside: false,
    });
    document.getElementById("top-navbar").style.zIndex="10001";
    document.getElementById("filtering-container").style.borderRadius = "5px";
    //document.getElementsByTagName("html")[0].style.overflow = "hidden";
    $('.filter-cursors').click(function () {
        swal.close();
        //document.getElementsByTagName("html")[0].style.overflow = "auto";
        document.getElementById("top-navbar").style.zIndex="10";
        document.getElementById("filter-box").style.zIndex="0";
        document.getElementById("filtering-container").style.borderRadius = "0px";
    });
}

// Disable arrow keys from changing the radio buttons
$('input[type="radio"]').keydown(function(e)
{
    var arrowKeys = [37, 38, 39, 40];
    if (arrowKeys.indexOf(e.which) !== -1)
    {
        $(this).blur();
        if (e.which == 38)
        {
            var y = $(window).scrollTop();
            $(window).scrollTop(y - 10);
        }
        else if (e.which == 40)
        {
            var y = $(window).scrollTop();
            $(window).scrollTop(y + 10);
        }
        return false;
    }
});

var currentLocation;
var locationString;

// populate calendar and get location of filter type.
function getLocation(event) {
    populate();
    var locationId = event.target.getAttribute('data-id');
    var locationName = event.target.innerHTML;
    var locationTitle = event.target.title;
    var locationAdr = document.getElementById("adr").innerText;
    this.currentLocation = locationId;
    this.locationString = locationName;
    var tooltip = document.createElement("div");
    tooltip.innerHTML = "&#9432;";
    tooltip.className = "tooltip-info";
    var tooltipText = document.createElement("span");
    tooltip.appendChild(tooltipText);
    tooltipText.className = "tooltip-text";
    tooltipText.innerHTML = locationTitle + "<br>" + "ADDR: " + locationAdr;
    document.getElementById("current-location").innerHTML = locationName;
    document.getElementById("current-location").appendChild(tooltip);
}

// Removes the calendar blur when filter is used
$('#search-button').click(function () {
    $('#calendar-container').css({
        'pointer-events': 'all',
        '-webkit-filter': 'blur(0px)',
        '-ms-filter': 'blur(0px)',
        'filter': 'blur(0px)',
    })
});

// Removes the calendar blur when filter is used
$('.filter-cursors').click(function (event) {

        getLocation(event)
        $('#calendar-container').css({
          'pointer-events': 'all',
          '-webkit-filter': 'blur(0px)',
          '-ms-filter': 'blur(0px)',
          'filter': 'blur(0px)',
      })

   });

// Removes the calendar blur when filter is used
$('.type-header').click(function (e) {
        dropdownFilters(e)
});