$(document).ready(function () {
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



});