var ContactForm = function () {

    return {

        //Contact Form
        initContactForm: function () {
            // Validation
            $("#createNewChatroomForm").validate({
                // Rules for form validation
                rules: {
                    chatroomName: {
                        required: true

                    },
                    chatroomDescription: {
                        required: true
                    },
                    chatroomMaxOccupants: {
                        required: true,
                        range: [2, 20]

                    },
                },

                // Messages for form validation
                messages: {
                    chatroomName: {
                        required: 'Name is required',
                    },
                    chatroomDescription: {
                        required: 'Description is required',
                    },
                    chatroomMaxOccupants: {
                        required: 'Max occupants must be 2-20'
                    },
                },

                // Ajax form submition
                submitHandler: function (form) {
                    console.log(form);
                    $("#createNewChatroomForm").submit(function (e) {
                        e.preventDefault();
                        $("#createNewChatroomForm").ajaxSubmit(
                            {
                                type: "POST",
                                dataType: "json",
                                url: "/api/v1/ownedchatrooms",
                                beforeSend: function () {

                                    //$('form button[type="submit"]').attr('disabled', true);

                                    var name = $("input[name=chatroomName]").val();
                                    var description = $("input[name=chatroomDescription]").val();
                                    var isPublic = false;
                                    var maxOccupants = $("input[name=chatroomMaxOccupants]").val();
                                    var token = $("input[name=csrfmiddlewaretoken]").val();
                                    var data = {
                                        "name": name,
                                        "description": description,
                                        "is_public": isPublic,
                                        "max_occupants": maxOccupants
                                    };


                                },
                                headers: {
                                    "X-CSRFToken": token
                                },
                                data: data,
                                success: function () {

                                    $("#createNewChatroomForm").addClass('submited');
                                }

                            }
                        );
                        return false;
                    });
                },

                // Do not change code below
                errorPlacement: function (error, element) {
                    error.insertBefore(element.parent());
                }
            });
        }

    };

}();