$(document).ready(function () {
    // $('.modal').modal();
    $('.collapsible').collapsible();
    $('select').formSelect();
    var dateToday = new Date();
    var dates = $("#user_date").datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 3,
        minDate: dateToday,
        onSelect: function (selectedDate) {
            var option = this.id == "from" ? "minDate" : "maxDate",
                instance = $(this).data("datepicker"),
                date = $.datepicker.parseDate(instance.settings.dateFormat || $.datepicker._defaults.dateFormat, selectedDate, instance.settings);
            dates.not(this).datepicker("option", option, date);
        }
    });

    function animateConfirmation() {
        $('.flash_wrap_request_edited, .flash_wrap_request_deleted').animate({
            opacity: '1'
        }, function () {
            $('.request_edited_text').animate({
                opacity: '1'
            });
        })
    }
    window.onload = animateConfirmation;



});