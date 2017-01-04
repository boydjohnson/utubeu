// get chatbox jquery object, make global so WebSockets.js can use it.
var $chatbox = $('#chat-box');

// apply the last ten messages for the chatroom into the chatbox
function chatbox_load_initial_message(messages){
    try{
        messages = JSON.parse(messages)
        var x = 0;
        var message = null;
        while(x < messages.last_ten.length){
            message = messages.last_ten[x];
            $chatbox.append("<p><span class='other'>"+message.user+"</span> " +message.text +"</p>");
            x++;
        }
    } catch (err){
        // if invalid json throws syntax error
        console.error(err);
    }
}