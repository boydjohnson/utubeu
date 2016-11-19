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
                    $(form).ajaxSubmit(
                        {
                            type: "POST",
                            dataType: "json",
                            url: "/api/v1/ownedchatrooms",
                            beforeSubmit: function (arr, $form, options ) {

                                $('form button[type="submit"]').attr('disabled', true);

                                var token = $("input[name=csrfmiddlewaretoken]").val();
                                arr.push({name:"is_public",value:"true"});
                                options.headers = {
                                    "X-CSRFToken": token
                                };

                            },
                            error:function(){
                                console.log("There was an error: woops");
                            },
                            success: function (data) {
                                console.log(data);
                                // sample response json {"id":3,"name":"Testing The Chatroom","description":"Description",
                                // "web_address":"localhost:8000/chatroom/testing-the-chatroom","is_public":true,
                                // "max_occupants":20,"last_video_thumb":null,
                                // "internal_identifier":"UiwbnyvsTxD3vd9qpvfdtz3S7FpYvM4nWl6w",
                                // "facebook_share": somelink,
                                // "twitter_share": someotherlink}
                                $("#createNewChatroomForm").addClass('submited');

                                $("#share-url").val(data.web_address);
                                $("#facebook_share").attr('href', data.facebook_share);
                                $("#twitter_share").attr('href', data.twitter_share);
                                $("#shareLinks").modal("toggle");

                            }

                        }
                    );

                    // this should break the normal submissions process
                    return false;

                },

                errorPlacement: function (error, element) {
                    error.insertBefore(element.parent());
                }
            });
        }

    };

}();