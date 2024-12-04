const functionBox = document.querySelector("div.function_box");
const darkPanel = document.querySelector("div.dark_panel");

if(darkPanel != null) {
    darkPanel.addEventListener("click", (event) => {
        const centerInformBox = document.querySelector("div.selectedFile_Box");
        if(!centerInformBox.contains(event.target)) {
            window.history.back();
        }
    });
}

if(functionBox !== null){
    const deleteButton = document.querySelector("button.delete_btn");

    const foldeName = functionBox.getAttribute("folderName");
    const fileName = functionBox.getAttribute("fileName");

    deleteButton.addEventListener("click", async() => {
        const result = await FileBoxFetch(`${ENV_HTTP_URL}:${PORT}/${foldeName}/${fileName}/delete_file`,"DELETE");
        
        if(result){
            window.location.href = `${ENV_HTTP_URL}:${PORT}/${foldeName}/`;
        }else {
            alert("관리자한테 문의 해주세요");
        }
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
        });

        const responseData = await response.json();
        console.log(responseData);
        
        if(responseData.success == "True"){
            return true;
        }else{
            return false;
        }
            
    }catch(err){
        throw err;
    }
}



