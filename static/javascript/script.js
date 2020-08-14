$(document).ready(function () {
    $('.sidenav').sidenav({
        edge: "right"
    });
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 3,
        showClearBtn: true,
        i18n: {
            done: "select"
        }
    });

    // Analog Clock

    const deg = 6;
    const hr = document.querySelector('#hr');
    const mn = document.querySelector('#mnt');
    const sec = document.querySelector('#sec');
    setInterval(() => {
        let day = new Date();
        let hh = day.getHours() * 30;
        let mm = day.getMinutes() * deg;
        let ss = day.getSeconds() * deg;
        hr.style.transform = `rotateZ($ {
                    hh + (mm / 12)
                }
                deg)`;
        mn.style.transform = `rotateZ(${mm}deg)`;
        sec.style.transform = `rotateZ(${ss}deg)`;
    }, 1000);


    // Digital time display
    function addZero(i) {
        if (i < 10) {
            i = "0" + i;
        }
        return i;
    }

    function timeUpdate() {
        var grabDate = new Date();
        var theTime = document.getElementById("the_time");
        var hours = addZero(grabDate.getHours());
        var minutes = addZero(grabDate.getMinutes());
        theTime.innerHTML = hours + ":" + minutes;
    }
    setInterval(timeUpdate, 1000);

});