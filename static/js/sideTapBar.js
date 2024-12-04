
// 새로고침의 경우
document.addEventListener("DOMContentLoaded", () =>{
    const is_open = localStorage.getItem("sideBar-state");

    if(is_open == "true"){
        openMenuBar();
    }
});

function openMenuBar(){
    let sideBar = document.getElementById("sideBar");
    let MenuIcon = document.getElementById("side_tap_bar");
    let backIcon = document.getElementById("backArrow");
    let headerContent = document.getElementById("headerContent")
    let mainContent = document.getElementById("mainContent");

    //상태 저장
    localStorage.setItem("sideBar-state", true);

    MenuIcon.parentElement.style.border = "0";
    sideBar.style.left = 0;
    MenuIcon.style.visibility = "hidden";
    backIcon.style.visibility = "visible";

    // 다른 태그의 width를 calc로 조절

    headerContent.style.width = "calc(100% - 300px)";
    mainContent.style.width = "calc(100% - 300px)";
}


function closeMenuBar(){
    let sideBar = document.getElementById("sideBar");
    let MenuIcon = document.getElementById("side_tap_bar");
    let backIcon = document.getElementById("backArrow");

    //상태 저장
    localStorage.setItem("sideBar-state", false);

    MenuIcon.parentElement.style.borderRight = "2px solid #474747";
    sideBar.style.left = "-300px";
    MenuIcon.style.visibility = "visible";
    backIcon.style.visibility = "hidden";

    // 다시 100%로 돌아감
    headerContent.style.width = "100%";
    mainContent.style.width = "100%";
}