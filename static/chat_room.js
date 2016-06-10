$(function() {
    $('#sendBtn').attr('disabled', true);

    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chat_room_uuid = $('#chat_room_uuid').val();
    var socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat/" + chat_room_uuid);
    socket.debug = true;
    socket.timeoutInterval = 6400;


    socket.onmessage = function(message) {
        console.log('on message....... : ', message);
        var data = JSON.parse(message.data);
        var chat_room_table = $("#chat_room_table")
        var table_row = $('<tr></tr>')

        table_row.append(
            $("<td></td>").text(data.created_dt)
        )
        table_row.append(
            $("<td></td>").text(data.sender)
        )
        table_row.append(
            $("<td></td>").text(data.message)
        )
        
        chat_room_table.prepend(table_row);
    };

    $("#chat_room_form").on("submit", function(event) {
        var message_element = $('#message');
        var message = {
            sender: $('#sender').val(),
            message: message_element.val(),
        }
        socket.send(JSON.stringify(message));
        
        $('#sendBtn').attr('disabled', true);
        message_element.val('')
        message_element.focus();
        
        return false;
    });

    enableSendBtn = function () {
        var message = $('#message').val();
        if (message == undefined || message == '' || message.length==0){
            $('#sendBtn').attr('disabled', true);
            
        } else{
            $('#sendBtn').attr('disabled', false);
        }
    }
});