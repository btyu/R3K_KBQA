// 发送提问请求
function send() {
    let text_type = document.getElementById("text-type");
    let text = text_type.value;
    text = text.trim();
    if(text === '')
        return;
    showText(text, 'sent');
    text_type.value = "";
    $.ajax({
        url: "/ask",
        type: "POST",
        data: JSON.stringify({
            text: text,
        }),
        contentType: "application/json",
        dataType: "json",
        success: function (data) {
            console.log('请求成功');
            processQueryNote(data.query_note);
        },
        error: function () {
            console.log("请求失败");
        }
    });
}

function processQueryNote(query_note_json) {
    let query_note = JSON.parse(query_note_json);
    showText(query_note['reply'], 'received');
}