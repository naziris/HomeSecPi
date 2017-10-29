//Change Password JavaScript Starts here -->
$( document ).ready(function() {
$('#editPasswordbtn').click(function() {
    $('#editPassword').modal('show');
    $('#editPasswordForm').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            password: {
                validators: {
                    notEmpty: {
                        message: 'The password is required and cannot be empty'
                    },
                    different: {
                        field: 'username',
                        message: 'The password cannot be the same as username'
                    },
                    stringLength: {
                        min: 8,
                        message: 'The password must have at least 8 characters'
                    },
                    identical: {
                        field: 'confirmPassword',
                        message: 'The password and its confirm are not the same'
                    }
                }
            },
            confirmPassword: {
                validators: {
                    notEmpty: {
                        message: 'The password is required and cannot be empty'
                    },
                    different: {
                        field: 'username',
                        message: 'The password cannot be the same as username'
                    },
                    stringLength: {
                        min: 8,
                        message: 'The password must have at least 8 characters'
                    },
                    identical: {
                        field: 'password',
                        message: 'The password and its confirm are not the same'
                    }
                }
            },
        }
    });
});
});
//Change Password JavaScript Ends here <--

//Change Username JavaScript Starts here -->
$( document ).ready(function() {
$('#editUsernamebtn').click(function() {
    $('#editUsername').modal('show');
    $('#editUsernameForm').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            username: {
                message: 'The username is not valid',
                validators: {
                    notEmpty: {
                        message: 'The username is required and cannot be empty'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'The username must be more than 6 and less than 30 characters long'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_]+$/,
                        message: 'The username can only consist of alphabetical, number and underscore'
                    }
                }
            },
        }
    });
});
});
//Change Username JavaScript Ends here <--

//Change e-Mail JavaScript Starts here -->
$( document ).ready(function() {
$('#editemailbtn').click(function() {
    $('#editemail').modal('show');
    $('#editemailForm').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            email: {
                validators: {
                    notEmpty: {
                        message: 'The email is required and cannot be empty'
                    },
                    emailAddress: {
                        message: 'The input is not a valid email address'
                    }
                }
            },
        }
    });
});
});
//Change e-Mail JavaScript Ends here <--

//Change Phone Number JavaScript Starts here -->
$( document ).ready(function() {
$('#editphoneNumberbtn').click(function() {
    $('#editphoneNumber').modal('show');
    $('#editphoneNumberForm').bootstrapValidator({
            // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                phoneNumber: {
                    validators: {
                        phone: {
                            country: 'countrySelectBox',
                            message: 'The value is not valid %s phone number'
                        }
                    }
                }
            }
        })
        .on('change', '[name="countrySelectBox"]', function(e) {
            $('#registrationForm').bootstrapValidator('revalidateField', 'phoneNumber');
        });
});
});
//Change Phone Number JavaScript Ends here <--

//Reset Password JavaScript Starts here -->
$( document ).ready(function() {
$('#confirmUsernamebtn').click(function() {
    $('#confirmUsername').modal('show');
    $('#confirmUsernameForm').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            username: {
                message: 'The username is not valid',
                validators: {
                    notEmpty: {
                        message: 'The username is required and cannot be empty'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'The username must be more than 6 and less than 30 characters long'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_]+$/,
                        message: 'The username can only consist of alphabetical, number and underscore'
                    }
                }
            },
        }
    });
});
});
//Reset Password  JavaScript Ends here <--

//shut down button starts here -->
$( document ).ready(function() {
    $('#digitPasswordsdbtn').click(function() {
        $('#digitPasswordsd').modal('show');
    });
    $(":input[type='tel']").keyup(function(event){
        if ($(this).next('[type="tel"]').length > 0){
            $(this).next('[type="tel"]')[0].focus();
        }else{
            if ($(this).parent().next().find('[type="tel"]').length > 0){
                $(this).parent().next().find('[type="tel"]')[0].focus();
            }
        }
    });
    $('#digitPasswordsd').on('shown.bs.modal', function (e) {
        $("#firstdigit").focus();
    });
});
//Shut Down button ends here <--

//Arm-Disarm button starts here -->
$( document ).ready(function() {
    $('#digitPasswordbtn').click(function() {
        $('#digitPassword').modal('show');
    });
    $(":input[type='tel']").keyup(function(event){
        if ($(this).next('[type="tel"]').length > 0){
            $(this).next('[type="tel"]')[0].focus();
        }else{
            if ($(this).parent().next().find('[type="tel"]').length > 0){
                $(this).parent().next().find('[type="tel"]')[0].focus();
            }
        }
    });
    $('#digitPassword').on('shown.bs.modal', function (e) {
        $("#firstdigit").focus();
    });
});
//Arm - Disarm Button ends here <--

//Change four-digit Password JavaScript Starts here -->
$( document ).ready(function() {
    $('#editFourDigitPasswordbtn').click(function() {
        $('#editFourDigitPassword').modal('show');
        $('#editFourDigitPasswordForm').bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            currentPassword: {
                validators: {
                    notEmpty: {
                        message: 'The password is required and cannot be empty'
                    },
                    stringLength: {
                        min: 4,
                        max: 4,
                        message: 'The password must be exactly four digits'
                    },
                }
            },
            newPassword: {
                validators: {
                    notEmpty: {
                        message: 'The password is required and cannot be empty'
                    },
                    different: {
                        field: 'currentPassword',
                        message: 'The password cannot be the same as current Password'
                    },
                    stringLength: {
                        max: 4,
                        min: 4,
                        message: 'The password must be exactly four digits'
                    },
                    identical: {
                        field: 'repeatNewPassword',
                        message: 'The password and its confirm are not the same'
                    }
                }
            },
            repeatNewPassword: {
                validators: {
                    notEmpty: {
                        message: 'The password is required and cannot be empty'
                    },
                    different: {
                        field: 'currentPassword',
                        message: 'The password cannot be the same as current Password'
                    },
                    stringLength: {
                        max: 4,
                        min: 4,
                        message: 'The password must be exactly four digits'
                    },
                    identical: {
                        field: 'newPassword',
                        message: 'The password and its confirm are not the same'
                    }
                }
            },
        }
    });
});
}); 
//Change four-digit Password JavaScript Ends here <--