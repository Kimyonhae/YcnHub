const listContent = document.querySelectorAll("div.side_bar_content li");
const edit_button_list = document.querySelectorAll("img.folder_edit");
const delete_button_list = document.querySelectorAll("img.folder_delete");
const VISIBLE_CLASS = "visibleClass";


async function fetchDataSubmit(baseUrl,title,method){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
        const response = await fetch(baseUrl,{
            method : method,
            headers : {
                "Content-Type" : "application/json",
                "X-CSRFToken" : csrftoken
            },
            body : JSON.stringify({'title' : title})
        }).then(response => response.json());
        console.log(response);
        if(response.status === "success"){ /* 성공 */
            window.location.href = '/';
        }else {
            alert(response.message);
        }
    }catch(e) {
        console.log(e);
        alert("문제가 생겼습니다.");
    }
}

// edit function
edit_button_list.forEach(editbutton => {
    editbutton.addEventListener("click", (event) => {
        const parentTag = editbutton.parentElement.parentElement; // li
        const inputValue = parentTag.querySelector('span'); // span
        // 삭제 
        editbutton.parentElement.classList.add(VISIBLE_CLASS); // folder_function 삭제
        inputValue.classList.add(VISIBLE_CLASS); // 값 삭제

        //생성
        let custom_input = document.createElement("input");
        custom_input.setAttribute("required", true);
        custom_input.setAttribute("placeholder", "수정 할 이름");
        custom_input.classList.add("createdInput");
        parentTag.appendChild(custom_input);
        custom_input.focus();
        // custom _Input이 Enter를 통해 서버에 data 전송.
        
        custom_input.addEventListener("keydown",(event) => {
            const folderName = editbutton.getAttribute("folderName");
            if(custom_input.value !== ""){
                if(event.key == 'Enter'){
                    fetchDataSubmit(`${ENV_HTTP_URL}:${PORT}/${folderName}/updateFolder/`,custom_input.value,"PATCH");
                }
            }
        });

        document.addEventListener("click",(event) => { // input을 제외한 것을 감지.
            event.preventDefault();

            if(event.target !== custom_input && event.target !== editbutton && custom_input){ // input의 외부
                // 태그 삭제
                parentTag.removeChild(custom_input);
                
                //초기화
                custom_input = null;

                // display
                editbutton.parentElement.classList.remove(VISIBLE_CLASS);
                inputValue.classList.remove(VISIBLE_CLASS);
                
                location.reload(); // 하이퍼링크 prevent를 refresh를 통해 해제.
            }
        });
    });
});



//delete function
delete_button_list.forEach(delete_button => {
    delete_button.addEventListener("click",(event) => {
        const folderName = delete_button.getAttribute("folderName");
        event.preventDefault();
        const qs = confirm("정말 지우시겠습니끼?");
        if(qs){
            fetchDataSubmit(`${ENV_HTTP_URL}:${PORT}/${folderName}/deleteFolder`,"","DELETE");
        }
    });
});
