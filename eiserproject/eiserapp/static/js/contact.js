$(document).ready(function() {
    "use strict";

    jQuery.validator.addMethod('answercheck', function (value, element) {
        return this.optional(element) || /^\bcat\b$/.test(value);
    }, "type the correct answer -_-");

    // validate contactForm form
    $('#contactForm').validate({
        rules: {
            subject: {
                required: true,
                minlength: 4
            },
            message: {
                required: true,
                minlength: 20
            }
        },
        messages: {
            subject: {
                required: "come on, you have a subject, don't you?",
                minlength: "your subject must consist of at least 4 characters"
            },
            message: {
                required: "um...yea, you have to write something to send this form.",
                minlength: "thats all? really?"
            }
        },
        submitHandler: function(form) {
            $.ajax({
                type: "POST",
                data: $(form).serialize(),
                url: "/contact_post/" + $("#userId").val(),
                success: function(response) {
                    if (response.status === "success") {
                        // Disable the form and show success modal
                        $('#contactForm :input').attr('disabled', 'disabled');
                        $('#contactForm').fadeTo("slow", 1, function() {
                            $('#success').fadeIn();
                            $('.modal').modal('hide');
                            $('#success').modal('show');
                        });
                        // Redirect to the appropriate page
                        window.location.href = response.redirect_url;
                    } else {
                        // Show error modal if response contains an error
                        $('#contactForm').fadeTo("slow", 1, function() {
                            $('#error').fadeIn();
                            $('.modal').modal('hide');
                            $('#error').modal('show');
                        });
                    }
                },
                error: function() {
                    $('#contactForm').fadeTo("slow", 1, function() {
                        $('#error').fadeIn();
                        $('.modal').modal('hide');
                        $('#error').modal('show');
                    });
                }
            });
        }
    });
});
