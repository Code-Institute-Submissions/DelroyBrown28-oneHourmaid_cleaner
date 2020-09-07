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

    // Initialize sign in input

    document.addEventListener('DOMContentLoaded', function () {
        var elems = document.querySelectorAll('.autocomplete');
        var instances = M.Autocomplete.init(elems, options);
    });

    function onLoadAnimations() {
        $('.account_title').animate({
            opacity: '1'
        }, function () {
            $('.cleaner_acc_tag').animate({
                opacity: '1'
            }, function () {
                $('#username_display').animate({
                    width: '100%'
                })
            })
        })

    }
    window.onload = onLoadAnimations;


    function animateConfirmation() {
        $('.confirmation_flash').animate({
            opacity: '1'
        }, function () {
            $('.confirmation_text').animate({
                opacity: '1'
            });
        })
    }
    window.onload = animateConfirmation;




});