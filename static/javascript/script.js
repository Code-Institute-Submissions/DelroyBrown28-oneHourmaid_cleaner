$(document).ready(function () {
    $('.modal').modal();
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


    // Service use text animation (main.html)

    setTimeout(function () {
        $('.serviceUseText_wrap').animate({
            width: '100%'
        }, function () {
            $('.service_use_text').animate({
                opacity: '1'
            })
        })

    }, 1000)


    // MOVING IN/OUT ICON ANIMATION

    $('.moving_out_check').click(function () {
        $('.moving_in_icon').animate({
            left: '50px'
        }, 300, function () {
            $('.moving_out_icon').animate({
                left: '0px'
            })
        })
    })

    $('.moving_in_check').click(function () {
        $('.moving_out_icon').animate({
            left: '-85px'
        }, 300, function () {
            $('.moving_in_icon').animate({
                left: '0px'
            })
        })
    })

  

});