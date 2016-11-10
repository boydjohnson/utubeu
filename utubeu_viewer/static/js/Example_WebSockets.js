var identifier = $('#chatroom').attr('data-chatroom');
var websockets = new WebSocket('ws://' + window.location.host +'/c/chat/' + identifier);



websockets.onopen = function (event) {
    console.log(event);
    websockets.send(JSON.stringify({'action': 'ChatMess', 'text': "Hello!"}));
};




websockets.onmessage = function(event){
   console.log(event.data);
    websockets.send(JSON.stringify({'action': 'Sugg', 'title': 'the best video ever!', 'video_id': '284knsodihg84w02nief',
                                 'imageurl': 'http://youtube.com/urlsomething', 'description': "the best video ever."}));

};