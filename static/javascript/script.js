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



    // Initialize sign in input

    document.addEventListener('DOMContentLoaded', function () {
        var elems = document.querySelectorAll('.autocomplete');
        var instances = M.Autocomplete.init(elems, options);
    });

});