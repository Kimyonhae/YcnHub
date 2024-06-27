const functionBox = document.querySelector("div.function_box");
const deleteButton = document.querySelector("button.delete_btn");
const fileContainer = document.querySelector("div.file_container");
const PAGE_RENDERING = "PAGE_RENDER";
if(functionBox !== null){
    const folderId = functionBox.getAttribute("folderId")
    const fileId = functionBox.getAttribute("fileId");

    deleteButton.addEventListener("click", () => {
        FileBoxFetch(`http://localhost:8000/${folderId}/${fileId}/delete_file`,"DELETE");
    });
}
async function FileBoxFetch(baseUrl , method , data){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
        const response = await fetch(baseUrl , {
            method  : method,
            headers : {
                "Content-Type" : "application/json",
                "X-CSRFToken" : csrftoken
            },
            body : data !== null ? data : null
        }).then(res => res.json());

        if(response){ /* 성공 */
            window.history.back();
            localStorage.setItem(PAGE_RENDERING, "true");
        }else {
            alert("관리자에게 문의 바랍니다.");
        }    
    }catch(err){
        throw err;
    }
}

window.onload = function(){
    const key = localStorage.getItem(PAGE_RENDERING);
    if(key == "true"){
        localStorage.removeItem(PAGE_RENDERING)
        window.location.reload();
    }
};