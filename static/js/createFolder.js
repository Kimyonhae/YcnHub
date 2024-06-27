const folder = document.querySelector("div.FolderInput"); // Folder Div click 태크
const folderInput = document.querySelector("input.folder_title"); // input 태크
const folderform = document.querySelector("form.folder_form");
const downloadBox = document.querySelector("div.selectedFile_Box");

folder.addEventListener("click",() => {
    folderform.classList.toggle("sidebar_visible");
    folderInput.focus();
});

folderInput.addEventListener("keydown", (event) => {
    if(event.key == 'Enter'){
        folderform.classList.add("sidebar_visible");
        console.log("Folder 창 열림 닫힘.");
    }
});

document.addEventListener("click", (event) => {
    // Input의 외부를 클릭 했을 경우 == 자손이 아닌 경우.
    if(!folder.contains(event.target) && !folderInput.contains(event.target)){
        folderform.classList.add("sidebar_visible");
    }
    if(downloadBox !== null){
        if(!downloadBox.contains(event.target)){
            window.history.back();
        }
    }
});