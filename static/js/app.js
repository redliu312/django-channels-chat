let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');

function updateUserList() {
    $.getJSON('api/v1/user/', function (data) {
        console.log(data)
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
            let userItem = `<a class="list-group-item user" id=${data[i]['id']}>${data[i]['username']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentRecipient(selected.text);
        });
    });
}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.user === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getConversation(recipient) {
    $.getJSON(`/api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}

function getMessageById(message) {
    id = JSON.parse(message).message
    console.log("message "+id)

    $.getJSON(`/api/v1/message/${id}/`, function (data) {
        console.log("data user"+data.user)

        $(`.list-group-item.user#${data.userid}`).addClass('active')
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {
    $.post('/api/v1/message/', {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('Error! Check console!');
    });
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}


function changeYoutubeIframeWithInput(){
    console.log("change");



}

function changeIfName() {
    inputUrl=$("#youtubeurlinput").val()
    console.log("change iframe src",inputUrl)


    var video_id = inputUrl.split('v=')[1];
var ampersandPosition = video_id.indexOf('&');
if(ampersandPosition != -1) {
  video_id = video_id.substring(0, ampersandPosition);
}
url = "https://www.youtube.com/embed/"+video_id;
player.loadVideoById(video_id);
return true;
}







$(document).ready(function () {
    updateUserList();
    disableInput();

    var socket = new WebSocket(
        'ws://' + window.location.host +
        '/ws?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
        }
    });


    socket.onmessage = function (e) {
        getMessageById(e.data);
    };

    });



