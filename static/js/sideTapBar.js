const VISIBLE_CLASS = "sidebar_visible"; // class 상수.
const SLIDER_CLASS = "sideBar_slide";
// menu img
const tabBar = document.querySelector("img#side_tap_bar");
// sideBar Content
const contentBar = document.querySelector("nav.side_bar_content");

const menuBar = document.querySelector("div.header_tap"); // menu img side_tap_bar header_tap

const testBackButton = document.querySelector("img.testback");
// 초기에 INIT_SIDERBAR 상태를 확인해서 조건을 세운다.
const checkTapState = localStorage.getItem("init-state"); //null | string


// localStorage 값이 "true"라면 사이드바를 숨깁니다.
if (checkTapState === "true") {
    contentBar.classList.remove(SLIDER_CLASS);
    // menu 이미지를 true일때 SideBar가 보이므로 이때 없애줌.
    menuBar.classList.add(VISIBLE_CLASS);

} else {
    // 그 외의 경우 (null 또는 "false"), 사이드바를 보여줍니다.
    contentBar.classList.add(SLIDER_CLASS);
    // menu 이미지를 false | null일떼 SideBar가 none , 이때 없애줌.
    menuBar.classList.remove(VISIBLE_CLASS);
}

function visibleHandle(){
    contentBar.classList.toggle(SLIDER_CLASS);
    if(!contentBar.classList.contains(SLIDER_CLASS)){ /* 사이드 바가 열린 경우. */
        localStorage.setItem("init-state", true);
        menuBar.classList.add(VISIBLE_CLASS);
    }else { // 사이드 바가 닫혀있습니다.
        localStorage.setItem("init-state", false);
        menuBar.classList.remove(VISIBLE_CLASS);
    }
}


tabBar.addEventListener("click",() => {
    visibleHandle(); 
});

testBackButton.addEventListener("click",() => {
    visibleHandle();
});

/*
    조건
    1. tabBar의 태그요소를 가져온다.  - clear
    
    2. onClick에 대한 event를 만들고 상태에 따라 조건 변경 즉 open , close가 서로 나눠줘야함. - clear
    
    3. 애니메이션 구현을 해야하는데...일단 위의 것 까지만 - progress
*/