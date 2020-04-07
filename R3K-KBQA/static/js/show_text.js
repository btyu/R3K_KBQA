// <div class="d-flex    justify-content-start    mb-4">
//     <div class="img_cont_msg">
//         <img class="rounded-circle    user_img_msg" src="{{ url_for('static', filename='assets/avatar1.png') }}" /></div>
//     <div class="msg_cotainer">Hi, how are you samim?</div>
// </div>

// <div class="d-flex    justify-content-end    mb-4">
//     <div class="msg_cotainer_send">Hi Maryam i am good tnx how about you?</div>
//     <div class="img_cont_msg">
//         <img class="rounded-circle    user_img_msg" src="{{ url_for('static', filename='assets/avatar2.png') }}"/>
//     </div>
// </div>

function getLine(text, type) {
    let pos_class_name, img_src, line_text_class_name;
    if (type === 'received') {
        pos_class_name = "d-flex    justify-content-start    mb-4";
        img_src = "static/assets/avatar1.png";
        line_text_class_name = "msg_cotainer";
    } else {
        pos_class_name = "d-flex    justify-content-end    mb-4";
        img_src = "static/assets/avatar2.png";
        line_text_class_name = "msg_cotainer_send";
    }

    let line = document.createElement('div');
    line.className = pos_class_name;
    let line_img = document.createElement('div');
    line_img.className = "img_cont_msg";
    let line_img_content = document.createElement('img');
    line_img_content.className = "rounded-circle    user_img_msg";
    line_img_content.setAttribute("src", img_src);
    line_img.appendChild(line_img_content);
    let line_text = document.createElement('div');
    line_text.className = line_text_class_name;
    line_text.innerText = text;

    if (type === 'received') {
        line.appendChild(line_img);
        line.appendChild(line_text);
    } else {
        line.append(line_text);
        line.append(line_img);
    }


    return line;
}

function showText(text, type) {
    let line_area = document.getElementById("line-area");
    let line = getLine(text, type);
    line_area.appendChild(line);
    updateScrolling(line_area);
}

function updateScrolling(scrolling_area) {
    // $(".msg_card_body").mCustomScrollbar({advanced:{ updateOnContentResize: true }});
    // $(".msg_card_body").mCustomScrollbar();
    // $('.msg_card_body').mCustomScrollbar('destroy').mCustomScrollbar("scrollTo", "bottom");
    // $("#line-area").mCustomScrollbar("update");
    scrolling_area.scrollTop = scrolling_area.scrollHeight;
}
